import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio
import google.generativeai as genai
from concurrent.futures import TimeoutError

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

max_iterations = 5
last_response = None
iteration = 0
iteration_response = []

async def generate_with_timeout(client, prompt, timeout=10):
    print("Generating with LLM...")
    try:
        loop = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(None, lambda: model.generate_content(prompt)),
            timeout=timeout
        )
        return response
    except TimeoutError:
        print("Timeout during LLM call")
        raise
    except Exception as e:
        print(f"LLM error: {e}")
        raise

def reset_state():
    global last_response, iteration, iteration_response
    last_response = None
    iteration = 0
    iteration_response = []

async def main():
    reset_state()
    try:
        server_params = StdioServerParameters(command="python", args=["example2.py"])

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools_result = await session.list_tools()
                tools = tools_result.tools

                tools_description = []
                for i, tool in enumerate(tools):
                    try:
                        params = tool.inputSchema
                        desc = getattr(tool, 'description', 'No description available')
                        name = getattr(tool, 'name', f'tool_{i}')

                        if 'properties' in params:
                            param_details = [f"{k}: {v.get('type', 'unknown')}" for k, v in params['properties'].items()]
                            params_str = ', '.join(param_details)
                        else:
                            params_str = 'no parameters'

                        tools_description.append(f"{i+1}. {name}({params_str}) - {desc}")
                    except:
                        tools_description.append(f"{i+1}. Error loading tool")
                tools_description = "\n".join(tools_description)

                system_prompt = f"""You are a problem-solving agent. You have access to tools for solving math problems and controlling Microsoft Paint.

TOOLS:
{tools_description}

RULES:
- You must respond with **EXACTLY ONE line**, starting with either FUNCTION_CALL: or FINAL_ANSWER:
- DO NOT return multiple lines.
- DO NOT call more than one function per response.
- Do NOT include explanations or comments.

ALLOWED FORMATS:
- FUNCTION_CALL: function_name|param1|param2|...
- FINAL_ANSWER: [your answer here]

EXAMPLES:
- FUNCTION_CALL: open_paint
- FUNCTION_CALL: draw_rectangle|780|380|1140|700
- FUNCTION_CALL: sqrt|144  
- FUNCTION_CALL: add_text_in_paint|AUTOMATED SUCCESS
- FINAL_ANSWER: [Done]

❗IMPORTANT:
- Only ONE function call per response.
- Do NOT chain calls.
- Do NOT return FUNCTION_CALL and FINAL_ANSWER together.

Respond with ONLY ONE valid line."""


                query = """Please open Paint, draw a rectangle from (780, 300) to (1140, 620), find the factorial of 8 and display it in a rectangle with relevant a quote from breaking bad."""

                global iteration, last_response
                while iteration < max_iterations:
                    print(f"\nIteration {iteration + 1}")
                    current_query = query if last_response is None else query + "\n\n" + " ".join(iteration_response) + "\nWhat should I do next?"

                    prompt = f"{system_prompt}\n\nQuery: {current_query}"
                    try:
                        response = await generate_with_timeout(client, prompt)
                        response_text = response.text.strip()
                        print(f"LLM Response: {response_text}")
                        for line in response_text.split('\n'):
                            line = line.strip()
                            if line.startswith("FUNCTION_CALL:"):
                                response_text = line
                                break
                    except Exception as e:
                        print(f"Error getting LLM response: {e}")
                        break

                    if response_text.startswith("FUNCTION_CALL:"):
                        _, function_info = response_text.split(":", 1)
                        parts = [p.strip() for p in function_info.split("|")]
                        func_name, params = parts[0], parts[1:]

                        try:
                            tool = next((t for t in tools if t.name == func_name), None)
                            if not tool:
                                raise ValueError(f"Unknown tool: {func_name}")

                            arguments = {}
                            schema = tool.inputSchema.get("properties", {})
                            for name, info in schema.items():
                                value = params.pop(0)
                                if info.get("type") == "integer":
                                    arguments[name] = int(value)
                                elif info.get("type") == "array":
                                    arguments[name] = [int(x.strip()) for x in value.strip("[]").split(',')]
                                else:
                                    arguments[name] = value

                            result = await session.call_tool(func_name, arguments=arguments)
                            if hasattr(result, "content"):
                                if isinstance(result.content, list):
                                    iteration_result = [item.text for item in result.content]
                                else:
                                    iteration_result = str(result.content)
                            else:
                                iteration_result = str(result)

                            if isinstance(iteration_result, list):
                                result_str = "[" + ", ".join(iteration_result) + "]"
                            else:
                                result_str = str(iteration_result)

                            iteration_response.append(
                                f"In Iteration {iteration+1}, called {func_name} with {arguments}, result: {result_str}"
                            )
                            last_response = iteration_result

                        except Exception as e:
                            print(f"Tool call failed: {e}")
                            break

                    elif response_text.startswith("FINAL_ANSWER:"):
                        print("Agent finished execution.")
                        print(response_text)
                        break

                    iteration += 1

    except Exception as e:
        print(f"Error in execution: {e}")
    finally:
        reset_state()

if __name__ == "__main__":
    asyncio.run(main())
