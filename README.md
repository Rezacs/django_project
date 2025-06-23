# Django IT Ticketing & Support Platform with GenAI Integration

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/django-4.2-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT4o-blueviolet)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📖 Overview

This project is a comprehensive IT ticketing and customer support platform, built with Django and enhanced by Generative AI (OpenAI GPT-4o). It is designed for IT support companies that manage IT needs for multiple client businesses (“sites”), allowing seamless issue reporting, live chat, AI-powered suggestions, and robust ticket tracking.

---

## 🚀 Key Features

- **Multi-Tenant Support:** One IT company supports many client companies (sites).
- **Roles & Permissions:** Engineers, Customers, and Admins with role-based access.
- **Ticket System:**  
  - Customers create and track tickets for their IT issues (internet, printers, software, etc.).
  - Engineers are auto-assigned based on site and expertise.
  - Tickets have lifecycle states and are fully auditable.

- **GenAI Integration:**  
  - **AI-powered Ticket Categorization:** GPT auto-tags new tickets for smarter routing.
  - **AI-Assisted Replies:** Engineers and users can chat with AI for instant troubleshooting advice and draft replies.
  - **Conversational History:** All user and AI messages are stored and viewable per ticket.

- **Live Chat:**  
  - Real-time messaging between users and AI (or with engineers, as extended).
  - Smart message display: clearly separates user vs. AI messages.

- **User Profile Management:**  
  - Change password, upload profile pictures, and leave service reviews.

- **Secure:**  
  - Login required for all core actions.
  - Each user can only see or edit their own or assigned tickets.

---

## 🏗️ System Architecture

- **Backend:** Django 4.x (Python 3.10+)
- **Frontend:** HTML, Bootstrap CSS, JavaScript (jQuery for AJAX if needed)
- **Database:** PostgreSQL or SQLite (development)
- **AI:** OpenAI GPT-4o via Python SDK
- **Deployment:** Supports local development; production-ready with minor changes

**Architecture Diagram:**  
