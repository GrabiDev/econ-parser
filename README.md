# Description
This script serves paid The Economist digital subscribers, who want to add The Economist Morning Briefing Full Edition to their Flash Briefings on an Alexa-enabled device.
There is an official `The Economist Morning Briefing` Alexa skill, but there is no way to sign into your paid subscription.
As a result, the official skill plays shorter briefing and contains ads.

To streamline the whole process, the app has been packaged into a Docker container.

The process of obtaining the custom link and deployment is fairly complex and not recommended for individuals without sufficient IT experience.
If you would like to use this solution but you are afraid of deploying it yourself, ask your techy friend for help.

# Additional information
The file processed by Alexa is served using [Surge](https://surge.sh/) free service.
The script downloads the Morning Briefing feed from The Economist, parses it to a form understandable by Alexa and uploads it to Surge hosting.

Steps below describe how to set up Surge hosting and connect it to your Alexa-enabled device.

For the best result for UK edition of The Economist, the script should be scheduled (e.g. as Cron job on Unix-like systems) to execute every day around 7:00am GMT.

Morning Briefing (and Espresso) come out every morning except Sundays.
This script addresses the issue by generating an empty feed on Sundays, preventing Alexa from playing the same briefing twice.

# Obtain The Economist Morning Briefing Full Edition custom link
1. Go to [briefing.economist.com](https://briefing.economist.com) in your web browser on your computer.
2. You might need to log in to your The Economist subscription.
3. You will either see a QR-code (desktop browsers) or a set of buttons to add the subscription to your apps (mobile browsers).
4. Right-click on the page and select `View Page Source` (name of the option might differ per browser).
5. Once you see source code of the page, press `Ctrl+F` on a PC or `Cmd+F` on a Mac.
6. Search for the string `access.acast.com`.
7. You should find something which looks like `"feedUrl":"http://access.acast.com/rss/theeconomistmorningbriefing/..."`.
   Dots will be replaced with you custom code.
8. Copy the whole URL found in the previous step (`http://...`) and save it somewhere on your computer.
   It will be needed for the next steps.

# Create Surge profile
1. Download and install [Node.js](https://nodejs.org/en/).
2. Run `npm install --global surge` (You might require root/administrator permissions on some systems).
3. Run `surge login` and follow instructions to log in or create account.

# Environmental variables
All of the variables below need to be defined in the container for the script to work:

| Variable      | Meaning                                                         | Sample value                       |
| ------------- | --------------------------------------------------------------- | ---------------------------------- |
| `BRIEFING_URL`| Your custom subscriber's URL to Morning Briefings Full Edition obtained in the previous steps. | `https://access.acast.com/rss/...` |
| `SURGE_LOGIN` | Email address you associated with your Surge account.           |  `john@example.com`                |
| `SURGE_TOKEN` | String of random letters and numbers displayed after executing `surge token` command. | `oXdqFHkdTngrtcECsucrkw6qGXw56SWrB` |
| `SURGE_DOMAIN`| URL under which you want to publish your processed feed.        |  `page-name.surge.sh`              |

There are also some optional settings available:

| Variable      | Meaning                                                         | Default value                      |
| ------------- | --------------------------------------------------------------- | ---------------------------------- |
| `WAIT_TIME_MINUTES`| Number of minutes to wait before retrying on an empty feed between Monday and Saturday.| `5` |
| `MAX_ATTEMPTS`| Maximum number of attempts when feed empty (`-1` for no limit). | `-1`                               |
| `MAX_RECONNECT_ATTEMPTS`| Maximum number of attempts when no connection with feed server (`-1` for no limit).  | `5` |
| `RECONNECT_TIME_MINUTES`| How long to wait before reconnecting attempt.         | `1`                                |

When using Docker, you can conveniently save them all in a single file in the following format and import them later:

```BRIEFING_URL=https://access.acast.com/rss/...
SURGE_LOGIN=john@example.com
SURGE_TOKEN=oXdqFHkdTngrtcECsucrkw6qGXw56SWrB
SURGE_DOMAIN=page-name.surge.sh
```

**Remember to replace above with your own values!**

Note down the location of your file with environmental variables.
It will be needed in the next step.

# Docker setup
Docker significantly simplifies deployment of this already complex solution.
Make sure Docker is installed on the machine on which you execute these steps.

Test your setup using the following steps:
1. Test your container by executing `docker run --rm --env-file /location/to/your/env-file grabidev/econ-parser:latest`, replacing `/location/to/your/env-file` with location of the file with environmental variables defined in the previous step.
2. If everything is correctly set up, you should see a confirmation from Surge CLI.
3. Open your web browser and navigate to your `briefing.xml` file somewhere online.
   Your URL probably looks similar to: `https://page-name.surge.sh/briefing.xml`
4. If you can see file with XML code and no errors, the script was successfully executed in the container.

Once you test your settings, deploy the container to a local Docker instance, such as a Raspberry Pi, on-premise or remote server or cloud environment.
No public IP address is required for the solution to work, thanks to the Surge service.

Depending on your setup, make sure `docker run --rm --name YOUR_CONTAINER_NAME --env-file /location/to/your/env-file grabidev/econ-parser:latest` is executed every morning.
Use your target operating system's best practices to schedule the job.

When executing the above command, logs are normally deleted together with the container when it exits due to `--rm` switch.
You might want to alter the command to connect it to your custom logging driver and persist container logs.

In Britain, the task should run around 7:00am GMT.
Regional editions of The Economist will have different release times for their briefings.

# Create a custom Alexa skill
In this step, you will create a custom Alexa skill to read your briefing.xml file and link it to your Flash Briefings. 

1. Create [Alexa Skill Blueprints](https://blueprints.amazon.com/) profile.
2. Click `Flash Briefings` on the main page.
3. Click `Create your own`.
4. Feel `Feed Name`, `Category` and `Introductory message` fields as you please.
5. Select `RSS` as the content format.
6. Paste path to the `briefing.xml` file on your Surge hosting.
   It probably looks like `https://page-name.surge.sh/briefing.xml`.
   **IMPORTANT:** Make sure the URL starts with `https`, not `http`!
7. Answer `Audio` to `Is your RSS feed audio or text?`.
7. Select `daily` update frequency.
8. Click `NEXT: NAME` button in the top right.
9. Give name to your new skill.
10. Click `NEXT: CREATE SKILL`.

**NOTE:** As access to the full Morning Briefings is based on your paid The Economist subscription, you should not publish this skill to Alexa store.
It might constitute a violation of your terms of subscription.

# Add your custom skill to your Alexa Flash Briefing
In this final step you will check if your custom Alexa skill was correctly added to your Alexa-enabled device.

1. Go to your Alexa app.
2. Tap top-left button for the menu and select `Skills & Games`.
3. Go to `Your Skills` tab and verify your skill is enabled.
4. Once again, go to the main menu and select `Settings`.
5. Select `Flash Briefings`.
6. Check if your new skill is on the list and is enabled.