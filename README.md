# DiscordBotPhoneLinkDialer

Demo video 2x normal speed.

https://github.com/user-attachments/assets/83916571-ea84-4468-8572-f05f3d3b1b38

## **What Is This Project?**

**DiscordBotPhoneLinkDialer** solves a personal problem: automating access to my barrier gate via phone calls, without needing manual intervention. The challenge comes from iOS restricts over certain actions, such as making automated phone calls, so I had to find a workaround.

By utilizing the [Phone Link](https://www.microsoft.com/en-us/windows/sync-across-your-devices?r=1) app on Windows, other people can remotely trigger calls to a predefined number from my phone without needing to manually intervene.

A Discord bot listens for messages in a server. When a message is received, the bot starts a screen recording (for debugging purposes) and initiates a GUI automation task. It opens the **Phone Link** app on Windows, dials a number preset by me, and makes the call. If the computer and phone are connected via Bluetooth and the Windows app establishes a link, it will trigger the phone call.

After the call is complete, the bot sends a feedback message asking the user whether the operation succeeded or failed. If the user reports a failure, the screen recording is uploaded to a separate debug channel for me to investigate the issue.

## **How to Run the Project**

### **Requirements**

Before running the project, make sure you have the following:

- A **Discord bot** and its **token**. [tutorial](https://www.ionos.com/digitalguide/server/know-how/creating-discord-bot/)
- The **Phone Link** app paired with your smartphone on your **Windows PC**.
- **Python 3.x** and **pip** installed.
- An **active Bluetooth connection** between your PC and smartphone.

### **Steps to Run the Project**

1. **Clone the repository**:
   First, clone the project repository to your local machine using Git:
   ```bash
   git clone https://github.com/vofr/DiscordBotPhoneLinkDialer.git
   cd DiscordBotPhoneLinkDialer
   ```
2. **Install dependencies**:
    Install the required Python libraries from the requirements.txt file
   ```bash
   pip install -r requirements.txt
   ```
3. **Create your env file**:
   Create a file named secrets.env in the project folder and add the following environment variables:
   ```env
   DISCORD_BOT_TOKEN=your-bot-token
   BARRIER_PHONE_NUMBER=the-phone-number-you-want-to-call
   ```
4. **Adjust GUI coordinates**:
   Update the following coordinates based on your screen and PhoneLink app layout:
   ```python
   PHONE_LINK_ICON
   CALL_BUTTON
   MINIMIZE_WINDOW
   ```
6. **Run the app**:
   Run the bot:
   ```bash
   python ./script.py
   ```



   
