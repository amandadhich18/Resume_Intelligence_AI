import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ==========================================
# MCP SERVER CONFIGURATION
# ==========================================

server_params = StdioServerParameters(
    command="python",
    args=["-m", "src.mcp_server"],
    cwd="D:\\Resume_Intelligence_AI"
)


# ==========================================
# MAIN MCP CLIENT
# ==========================================

async def main():

    print("=" * 60)
    print("MCP CLIENT → MCP SERVER TEST")
    print("=" * 60)

    # Start MCP server through STDIO
    async with stdio_client(server_params) as (
        read_stream,
        write_stream
    ):

        # Create MCP client session
        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            # ----------------------------------
            # INITIALIZE MCP CONNECTION
            # ----------------------------------

            await session.initialize()

            print("\n✅ MCP server connected")

            # ----------------------------------
            # LIST AVAILABLE TOOLS
            # ----------------------------------

            tools_result = await session.list_tools()

            print("\nAvailable MCP tools:")

            for tool in tools_result.tools:

                print(
                    f"- {tool.name}: "
                    f"{tool.description}"
                )

            # ----------------------------------
            # CALL TOOL 1
            # ----------------------------------

            print("\n" + "-" * 60)
            print("CALLING: extract_job_description_skills")
            print("-" * 60)

            jd_text = """
            We are looking for a Data Analyst
            with Python, SQL, Power BI,
            Tableau and Excel experience.
            """

            result = await session.call_tool(
                "extract_job_description_skills",
                {
                    "job_description": jd_text
                }
            )

            print("\nJD Skill Extraction Result:")
            print(result)

            # ----------------------------------
            # CALL TOOL 2
            # ----------------------------------

            print("\n" + "-" * 60)
            print("CALLING: match_resume_with_job")
            print("-" * 60)

            resume_skills = [
                "Python",
                "SQL",
                "Power BI",
                "Excel"
            ]

            jd_skills = [
                "Python",
                "SQL",
                "Power BI",
                "Tableau",
                "Excel"
            ]

            result = await session.call_tool(
                "match_resume_with_job",
                {
                    "resume_skills": resume_skills,
                    "job_description_skills": jd_skills
                }
            )

            print("\nResume ↔ JD Matching Result:")
            print(result)

            # ----------------------------------
            # SUCCESS
            # ----------------------------------

            print("\n" + "=" * 60)
            print("MCP CLIENT TEST COMPLETED SUCCESSFULLY")
            print("=" * 60)


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":
    asyncio.run(main())