import os
import coc
import asyncio
from dotenv import load_dotenv
import json

# Import only the function you need from your other file
from clandata import update_data

async def main():
    """
    Main function to handle client session, login, and data fetching.
    """
    # 1. Load configuration from .env file
    load_dotenv()
    COC_EMAIL = os.getenv("COC_EMAIL")
    COC_PASSWORD = os.getenv("COC_PASSWORD")
    CLAN_TAG = os.getenv("CLAN_TAG")

    if not all([COC_EMAIL, COC_PASSWORD, CLAN_TAG]):
        print("Error: Make sure COC_EMAIL, COC_PASSWORD, and CLAN_TAG are set in your .env file.")
        return

    # 2. Create a single, managed client session
    # This block ensures the client is active for all the operations inside it.
    async with coc.Client() as client:
        try:
            # 3. Log in using the client
            await client.login(COC_EMAIL, COC_PASSWORD)
            print("Login successful!")

            # 4. Call your function with the ACTIVE client
            # Use 'await' because get_clan_data is an async function.
            clan_data = await update_data(client, CLAN_TAG)

            # 5. Process the results
            if clan_data:
                # --- THIS LINE IS NOW CORRECTED ---
                # It now looks inside the dictionary to get the member count.
                member_count = len(clan_data["memberInfo"])
                print(f"\nSuccessfully retrieved data for {member_count} members.")
                
                with open("clan_data.json", "w") as f:
                    json.dump(clan_data, f, indent=4)
                print("Data saved to clan_data.json")
            else:
                print("\nCould not retrieve any clan data.")

        except coc.InvalidCredentials as error:
            print(f"Login failed: {error}")
        except Exception as e:
            print(f"A critical error occurred in the main loop: {e}")

# This is the standard entry point to run your async main function.
if __name__ == "__main__":
    print("Script running!")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
        

    

