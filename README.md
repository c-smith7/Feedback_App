![Badge](https://img.shields.io/badge/Project%20Status-Completed-blue)
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/c-smith7/VIPKid_Feedback_App/blob/main/LICENSE.txt)


<br />
  <p align="center">
  <a href="https://github.com/c-smith7/Feedback_App">
    <img src="icons/pencil_432x432.png" alt="Logo" width="90" height="90">
  </a>

  <h1 align="center">Feedback App</h1>

  <p align="center">
    A real-time webscraper that automates custom client feedback.
    <br />
    <a href="https://github.com/c-smith7/Feedback_App/issues">Report Bug</a>
    ·
    <a href="https://github.com/c-smith7/Feedback_App/issues">Request Feature</a>
  </p>
</p>
    
<details open>
  <summary><h3 style="display: inline-block">Table of Contents</h3></summary>
  <ol>
    <li>
      <a href="#about">About</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#google-chrome">Google Chrome</a></li>
        <li><a href="#installation-and-run">Installation and Run</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contribute">Contribute</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About

The Feedback App was created to automate my workflow during my time as an online freelance teacher. Specifically, I wanted to automate the process of providing daily feedback to students, which was very tedious and time consuming when doing by hand.  

After creating the Feedback App, I was able to save about 1-2 hours of work per day. This translated into me earning about $4 extra on my hourly rate.  

Ultimately, the goal was to save time and money. For me, it achieved this goal.  I hope it does the same for you.

### Built With..

* [Python 3](https://www.python.org/downloads/)
* [PyQt5](https://pypi.org/project/PyQt5/5.12.3/)
* [Selenium](https://selenium-python.readthedocs.io/)

## Getting Started

### Google Chrome
This app currently requires Google Chrome in order to perform the webscraping. However, Chrome does not need to be running when using the Feedback App, only installed on the machine. Follow the link to download the [latest version](https://www.google.com/chrome/) if needed.
<br></br>
(Chrome version used for this app was: 92.0.4515.159)
<br></br>
If the latest version of Chrome raises an issue when trying to run the app, this means that the [chromedriver](https://chromedriver.chromium.org/) needs to be updated to the latest version. Follow the link to download the latest version of chromedriver. 

### Installation and Run

1. Clone the project

    ```
    git clone https://github.com/c-smith7/Feedback_App.git
    ```
2. Go to the project directory

    ```
    cd Feedback_App
    ```
3. Install requirements
    ```
    python -m pip install -r requirements.txt
    ```
4. Run the app
    ```
    python main.py
    ```

## Usage

Here is a [usage tutorial](https://www.youtube.com/watch?v=nsJ5m8Drx-g) for the app, which shows how I use it in my daily workflow. 

You can also visit my website, [databycarl.com](https://databycarl.com/feedback-app/), where you can find more demos of the app, which show how much time the app saves me. 

Step-by-step guide of how to use the app:  
1. Login to your VIPKid account by pressing "Login" button. 
    * When you login for the first time, you will be prompted to enter your login info.. The next time you use the app, you can simply press the "Login" button and you will logged in automatically. 
    * If you do not want to be logged in automatically the next time you use the app, simply go to File>Logout, when you are finished using the app.  
2. Press the "Get Feedback Template" button.
    * This will automatically search for and return the name and templates to use for the first student on your missing feedback page.  
3. Select "Yes" or "No" to specify whether the current student is new or not. 
4. Press "Generate Feedback" button.
    * This will generate the final custom feedback, using the student's name and feedback signature.
    * You can edit the feedback signatures in the "Edit" menu, Edit>Edit Feedback Signatures. There are two signatures you can set, one for recurring students (Default Signature) and one for new students (New Student Signature).
5. Press the "Copy Feedback" button.  
    * This will copy the generated feedback to your clipboard. Where you can then paste wherever you'd like. 

## Contribute
1. Fork the project.
2. Create a new branch for your feature: 
    ```
    git checkout -b feature/your-feature-name
    ```
3. Commit your changes/feature:
    ``` 
    git commit -am 'Brief description of your changes.'
    ```
4. Push to the branch:
    ```
    git push origin feature/your-feature-name
    ```
5. Open a [Pull Request](https://github.com/c-smith7/Feedback_App/pulls).

## License

Distributed under the MIT License. See `License.txt` for more information.

  
##  Contact
[![portfolio](https://img.shields.io/badge/my_portfolio-999?style=for-the-badge&logo=ko-fi&logoColor=white)](https://databycarl.com/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/)
[![Gmail Badge](https://img.shields.io/badge/carlvsmith7-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:carlvsmith7@gmail.com)
[![Twitter Badge](https://img.shields.io/badge/@cvsmith__7-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/messages/compose?recipient_id=245625455)  

  
