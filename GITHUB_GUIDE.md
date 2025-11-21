# How to Upload Your Project to GitHub

## Step 1: Install Git (If not installed)
1.  Download Git from [git-scm.com](https://git-scm.com/downloads).
2.  Install it (just click Next, Next, Next...).
3.  Open your terminal (Command Prompt or PowerShell) and check if it works:
    ```bash
    git --version
    ```

## Step 2: Create a Repository on GitHub
1.  Go to [github.com](https://github.com) and log in.
2.  Click the **+** icon in the top right and select **New repository**.
3.  **Repository name**: `face-attendance-system` (or whatever you like).
4.  **Public/Private**: Choose Public (everyone can see) or Private (only you).
5.  **Do NOT** check "Add a README file" (we already have one).
6.  Click **Create repository**.

## Step 3: Upload Your Code
Open your terminal inside your project folder (`c:\Users\shakh\OneDrive\Desktop\face_attendi4`) and run these commands one by one:

1.  **Initialize Git**:
    ```bash
    git init
    ```

2.  **Add your files**:
    ```bash
    git add .
    ```
    *(This stages all your files. Don't worry, I created a `.gitignore` file so it won't upload your photos, database, or large models.)*

3.  **Commit your changes**:
    ```bash
    git commit -m "Initial commit - Face Attendance System V1"
    ```

4.  **Link to GitHub** (Replace `YOUR_USERNAME` with your actual GitHub username):
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/face-attendance-system.git
    ```
    *(You can copy this exact line from the page you saw after creating the repo on GitHub)*

5.  **Push the code**:
    ```bash
    git branch -M main
    git push -u origin main
    ```

## Step 4: You're Done!
Refresh your GitHub page, and you should see your code there!

---
**Note:**
- I have excluded `attendance.db` (your database) and `enrollment_images/` (your photos) for privacy.
- I have excluded `models/` because they are too large for GitHub. The `download_models.py` script allows anyone to download them again.
