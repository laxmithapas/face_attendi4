# 🔒 Privacy Policy & Data Handling

**Effective Date:** November 2025

## 1. Introduction
This Privacy Policy explains how the **Face Recognition Attendance System** collects, uses, and protects biometric data. We are committed to ensuring the security and privacy of all enrolled users.

## 2. Data We Collect
*   **Personal Information:** Name and Email Address.
*   **Biometric Data:** Facial Encodings (mathematical representations of the face).
*   **Attendance Logs:** Dates, Times, and Duration of presence.
*   **Audit Logs:** Records of administrative access (Login Success/Failure) and critical system actions.

## 3. How We Use Data
*   **Authentication:** To verify identity during attendance marking.
*   **Analytics:** To generate attendance reports and punctuality scores.
*   **Security:** To detect and prevent fraud (Liveness Detection) and unauthorized access (Audit Trails).

## 4. Data Storage & Security
*   **Encryption:** All facial encodings are **Encrypted** using Fernet (symmetric encryption) before being stored in the database.
*   **Local Storage:** Data is stored locally on the secure server/machine. No data is uploaded to the cloud.
*   **Access Control:** The Admin Dashboard is password-protected.
*   **Session Security:** Administrators are automatically logged out after **5 minutes of inactivity** to prevent "shoulder surfing" or unauthorized access.

## 5. Data Retention & Deletion
*   **Retention:** Data is retained only as long as the user is an active member of the organization.
*   **Deletion:** Administrators can permanently delete a user's profile via the Dashboard. This action performs a **Secure Delete**, removing:
    *   Database records (Profile & Logs).
    *   Biometric Encodings.
    *   Stored Reference Images.

## 6. Compliance
This system is designed with privacy-by-design principles, suitable for educational and internal corporate use.

---

**Contact:** [Your Name/Department]
