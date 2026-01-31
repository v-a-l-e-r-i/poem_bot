# **📂 Telegram Bot: Provulok (Submission Manager)**

This bot is designed to automate the submission of creative works (poetry, prose, visual art) for the Telegram channel **"Provulok"** (*The Lane*). The bot collects data from users, saves it to a spreadsheet (Google Sheets), and notifies authors about moderation results.

## **📑 Table of Contents**

* [Key Features](https://www.google.com/search?q=%23-key-features)  
* [Technical Requirements](https://www.google.com/search?q=%23-technical-requirements)  
* [Installation and Setup](https://www.google.com/search?q=%23-installation-and-setup)  
* [Configuration](https://www.google.com/search?q=%23-configuration-env)  
* [Database Structure](https://www.google.com/search?q=%23-database-structure-google-sheets)  
* [Dialogue Scenario](https://www.google.com/search?q=%23-dialogue-scenario)  
* [Notifications](https://www.google.com/search?q=%23-notifications-scheduler)

## **📋 Key Features**

### **👤 For the User (Author)**

* **Sequential Dialogue:** The bot guides the user step-by-step (no complex commands required).  
* **Data Collection:**  
  1. Receiving the file or text of the creative work.  
  2. Input of the author's name/pseudonym.  
  3. Input of social media links (or skipping this step).  
* **Feedback:** Receiving notifications about publication or rejection.

### **🛡️ For the Administrator (Editorial Team)**

* **Convenient Moderation:** Administrators do not interact directly with the bot. All work is done via **Google Sheets**.  
* **Status Management:** Decisions are made by changing the status cell in the spreadsheet.  
* **Automation:** The bot periodically (e.g., every 3 days) checks the spreadsheet and sends notifications to authors whose status has changed.

## **🛠 Technical Requirements**

* **Python** (version 3.9+)  
* **aiogram** (for working with Telegram API)  
* **gspread / google-api-python-client** (for working with Google Sheets)  
* **apscheduler** (for scheduling status checks every 3 days)

## **🚀 Installation and Setup**

1. **Clone the repository:**  
   git clone [https://github.com/v-a-l-e-r-i/poem_bot.git](https://github.com/v-a-l-e-r-i/poem_bot.git)
   cd provulok-bot

2. **Create a virtual environment and activate it:**  
   python \-m venv venv  
   source venv/bin/activate  \# For Windows: venv\\Scripts\\activate

3. **Install dependencies:**  
   pip install \-r requirements.txt

4. Configure environment variables:  
   Create a .env file and add the necessary keys (see example below).  
5. **Run the bot:**  
   python main.py

## **⚙️ Configuration (.env)**

Create a .env file in the root folder of the project:

BOT\_TOKEN=your\_token\_from\_BotFather  
GOOGLE\_SHEETS\_CREDENTIALS=path\_to\_credentials.json  
GOOGLE\_SHEET\_ID=your\_google\_sheet\_id  
ADMIN\_IDS=12345678,87654321  
CHECK\_INTERVAL\_DAYS=3

## **📊 Database Structure (Google Sheets)**

The bot expects the Google Sheet to have the following columns (order is important, or binding by name):

| Field | Description | Notes |
| :---- | :---- | :---- |
| **user\_id** | User's Telegram ID | Filled by the bot |
| **username** | Telegram username | If available, otherwise None |
| **work\_content** | Text of the work or file link | Text or file\_id/URL |
| **author\_name** | Name / Pseudonym | Provided by the user |
| **social\_links** | Social media links | Links or "-" |
| **submit\_date** | Submission date | DD.MM.YYYY HH:MM |
| **status** | Application status | pending / accepted / rejected |
| **decision\_date** | Decision date | Filled when status changes |

### **Application Statuses (status field)**

* pending — (Default) Awaiting review.  
* accepted — Accepted. The bot will send a congratulatory message.  
* rejected — Rejected. The bot will send a rejection message.

## **💬 Dialogue Scenario**

The bot communicates in a friendly tone ("informal/friendly").

1. **Start:***«Welcome to Provulok\! Send us your creative work (poem, free verse, prose, visual art)»*  
2. **After receiving the file/text:***«We received your work\! Now write how you would like to be signed 🥰»*  
3. **After entering the name:***«Beautiful name\! If you wish to leave your social media links with your art – do it now\! (If you don't have any – type "-")»*  
4. **Finale:***«Thank you\! We will notify you soon\! Until next time, friend»*

## **🔔 Notifications (Scheduler)**

The bot runs a background process to check the table (default — every 3 days).

* **If status changed to accepted:***«Congratulations, author\! Your work will be in the Provulok channel. Publication may take from one to three days. Thank you\!»*  
* **If status changed to rejected:***«Unfortunately, your work was not accepted. But don't be sad – next time it will work out\!»*

## **📝 License**

This project was developed specifically for the "Provulok" channel.
