# CTF-Challenges | Capture The Flag Lab

## Overview
This is my fifth cybersecurity lab project where I designed and deployed **CTF (Capture The Flag) challenges**.  
The goal was to practice problem-solving, offensive security, and challenge creation for learning and skill development.

---

## Tools & Technologies
- **Virtualization:** VMware Workstation Pro  
- **Operating Systems:** Ubuntu Server, Windows 10 (for challenge hosting)  
- **CTF Platforms/Tools:**  
  - PicoCTF, CTFd (web-based CTF platform)  
  - Burp Suite, Nmap, Wireshark, Netcat  
  - Python & Bash for challenge scripts  
- **Other Tools:** GitHub (for challenge repository), Docker (optional for isolation)  

---

## Lab Setup
I set up a safe environment to host challenges:

| Component       | Purpose |
|----------------|---------|
| CTF Platform    | Host challenges, track flags, manage users |
| Challenge VMs  | Contain vulnerable programs, web apps, or services |
| Attacker VM    | Used to test challenges and verify solutions |
| Network/Isolation | Ensures challenges don’t affect the main network |

- Each challenge is **isolated** in a VM or Docker container.  
- Flags are hidden in files, services, or scripts for participants to find.  

---

## Example Challenges
1. **Web Challenge:** Exploit a vulnerable web form to retrieve the flag.  
2. **Reverse Engineering:** Analyze a small binary to extract a hidden key.  
3. **Networking:** Capture packets and find the secret data.  
4. **Cryptography:** Decode a message using given hints and tools.  
5. **Scripting:** Write a Python/Bash script to solve a puzzle or automate a task.  

---

## Setup Steps
1. **Create VMs** in VMware Workstation Pro for the platform and challenges.  
2. **Install Ubuntu Server** for CTF platform hosting.  
3. **Install CTFd** or a similar platform to manage challenges.  
4. **Develop challenges** (web, crypto, reverse engineering, networking).  
5. **Test each challenge** using an attacker VM to ensure flags are reachable.  
6. **Document challenges** and solutions in README files for future reference.  

---

## Screenshots / Proof
*(I added screenshots of the CTF dashboard, challenge setup, and solved flags.)*  

- CTFd platform showing challenges and flags  
- Example solved challenge output  
- Network capture of a challenge exploitation  

---

## Learning Notes
- I learned how to **design challenges** that teach security concepts.  
- Testing challenges helped me **think like an attacker** and understand exploits.  
- Documenting solutions strengthened my **technical communication skills**.  
- Hosting challenges taught me **platform setup, isolation, and security best practices**.  

---

## Next Steps
- Add more **complex challenges** in web security, cryptography, and reverse engineering.  
- Automate challenge deployment with **Docker or scripts**.  
- Share challenges with friends or an online CTF community for feedback.  

---

**Author:** Ayoub Khachane
