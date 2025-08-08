import streamlit as st
import psutil
import requests
import json
import time
import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from datetime import datetime
import webbrowser
import urllib.parse
from bs4 import BeautifulSoup


def run():
    st.title("🐍 Python Multi-Tool Dashboard")
    st.markdown("A comprehensive collection of Python utilities and automation tools")

    st.sidebar.title("🛠️ Available Tools")
    
    tool_category = st.sidebar.selectbox(
        "Select Category:",
        ["📊 System Tools", "📱 Communication", "🌐 Web & Social", "🎨 Media & Graphics", "🤖 AI & Automation"]
    )
    
    if tool_category == "📊 System Tools":
        show_system_tools()
    elif tool_category == "📱 Communication":
        show_communication_tools()
    elif tool_category == "🌐 Web & Social":
        show_web_social_tools()
    elif tool_category == "🎨 Media & Graphics":
        show_media_graphics_tools()
    elif tool_category == "🤖 AI & Automation":
        show_ai_automation_tools()

def show_system_tools():
    st.header("📊 System Tools")
    
    st.subheader("💾 RAM Usage Monitor")
    
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total RAM", f"{ram.total / (1024**3):.2f} GB")
        st.metric("Available RAM", f"{ram.available / (1024**3):.2f} GB")
    
    with col2:
        st.metric("RAM Usage %", f"{ram.percent:.1f}%")
        st.metric("Used RAM", f"{ram.used / (1024**3):.2f} GB")
    
    with col3:
        st.metric("Swap Total", f"{swap.total / (1024**3):.2f} GB")
        st.metric("Swap Used", f"{swap.used / (1024**3):.2f} GB")
    
    st.subheader("📈 RAM Usage Over Time")
    
    if 'ram_history' not in st.session_state:
        st.session_state.ram_history = []
    
    st.session_state.ram_history.append({
        'time': datetime.now().strftime('%H:%M:%S'),
        'usage': ram.percent
    })
    
    if len(st.session_state.ram_history) > 20:
        st.session_state.ram_history = st.session_state.ram_history[-20:]
    
    if st.session_state.ram_history:
        times = [entry['time'] for entry in st.session_state.ram_history]
        usage = [entry['usage'] for entry in st.session_state.ram_history]
        
        chart_data = {
            'Time': times,
            'RAM Usage %': usage
        }
        
        st.line_chart(chart_data)
    
    st.subheader("🖥️ System Information")
    
    col1, col2 = st.columns(2)

    with col1:
        st.write("**CPU Information:**")
        st.write(f"CPU Count: {psutil.cpu_count()}")
        st.write(f"CPU Usage: {psutil.cpu_percent(interval=1)}%")
        
        st.write("**Disk Information:**")
        disk = psutil.disk_usage('/')
        st.write(f"Total: {disk.total / (1024**3):.2f} GB")
        st.write(f"Used: {disk.used / (1024**3):.2f} GB")
        st.write(f"Free: {disk.free / (1024**3):.2f} GB")

    with col2:
        st.write("**Network Information:**")
        network = psutil.net_io_counters()
        st.write(f"Bytes Sent: {network.bytes_sent / (1024**2):.2f} MB")
        st.write(f"Bytes Received: {network.bytes_recv / (1024**2):.2f} MB")
        
        st.write("**Boot Time:**")
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        st.write(f"System Boot: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")

def show_communication_tools():
    st.header("📱 Communication Tools")
    
    st.subheader("📧 Email Sender")
    
    with st.expander("Email Configuration"):
        smtp_server = st.text_input("SMTP Server:", value="smtp.gmail.com")
        smtp_port = st.number_input("SMTP Port:", value=587)
        sender_email = st.text_input("Sender Email:")
        sender_password = st.text_input("Sender Password:", type="password")
    
    recipient_email = st.text_input("Recipient Email:")
    subject = st.text_input("Subject:")
    message = st.text_area("Message:")
    
    if st.button("📧 Send Email"):
        if sender_email and sender_password and recipient_email and message:
            try:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient_email
                msg['Subject'] = subject
                
                msg.attach(MIMEText(message, 'plain'))
                
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)
                text = msg.as_string()
                server.sendmail(sender_email, recipient_email, text)
                server.quit()
                
                st.success("✅ Email sent successfully!")
            except Exception as e:
                st.error(f"❌ Error sending email: {str(e)}")
        else:
            st.warning("⚠️ Please fill in all required fields")
    
    st.subheader("📱 WhatsApp Messenger")
    
    phone_number = st.text_input("Phone Number (with country code):", placeholder="+1234567890")
    whatsapp_message = st.text_area("WhatsApp Message:")
    
    if st.button("📱 Send WhatsApp Message"):
        if phone_number and whatsapp_message:
            try:
                import pywhatkit as pwk
                pwk.sendwhatmsg_instantly(phone_number, whatsapp_message, 15, True, 3)
                st.success("✅ WhatsApp message scheduled!")
            except Exception as e:
                st.error(f"❌ Error sending WhatsApp message: {str(e)}")
                st.info("Note: PyWhatKit requires a display connection. This feature works best in desktop environments.")
        else:
            st.warning("⚠️ Please enter phone number and message")
    
    st.subheader("📱 SMS Sender (Twilio)")
    
    with st.expander("Twilio Configuration"):
        twilio_account_sid = st.text_input("Twilio Account SID:")
        twilio_auth_token = st.text_input("Twilio Auth Token:", type="password")
        twilio_phone_number = st.text_input("Twilio Phone Number:")
    
    sms_phone_number = st.text_input("Recipient Phone Number:")
    sms_message = st.text_area("SMS Message:")
    
    if st.button("📱 Send SMS"):
        if twilio_account_sid and twilio_auth_token and twilio_phone_number and sms_phone_number and sms_message:
            try:
                from twilio.rest import Client
                
                client = Client(twilio_account_sid, twilio_auth_token)
                message = client.messages.create(
                    body=sms_message,
                    from_=twilio_phone_number,
                    to=sms_phone_number
                )
                
                st.success(f"✅ SMS sent successfully! SID: {message.sid}")
            except Exception as e:
                st.error(f"❌ Error sending SMS: {str(e)}")
        else:
            st.warning("⚠️ Please fill in all Twilio configuration fields")
    
    st.subheader("📞 Phone Call (Twilio)")
    
    call_phone_number = st.text_input("Phone Number to Call:")
    call_message = st.text_area("Message to Speak:")
    
    if st.button("📞 Make Phone Call"):
        if twilio_account_sid and twilio_auth_token and twilio_phone_number and call_phone_number and call_message:
            try:
                from twilio.rest import Client
                
                client = Client(twilio_account_sid, twilio_auth_token)
                call = client.calls.create(
                    twiml=f'<Response><Say>{call_message}</Say></Response>',
                    from_=twilio_phone_number,
                    to=call_phone_number
                )
                
                st.success(f"✅ Phone call initiated! Call SID: {call.sid}")
            except Exception as e:
                st.error(f"❌ Error making phone call: {str(e)}")
        else:
            st.warning("⚠️ Please fill in all required fields")

def show_web_social_tools():
    st.header("🌐 Web & Social Media Tools")
    
    st.subheader("🔍 Google Search")
    
    search_query = st.text_input("Search Query:")
    num_results = st.number_input("Number of Results:", min_value=1, max_value=20, value=5)
    
    if st.button("🔍 Search Google"):
        if search_query:
            try:
                from googlesearch import search
                
                results = []
                for url in search(search_query, num_results=num_results):
                    results.append(url)
                
                st.write("**Search Results:**")
                for i, url in enumerate(results, 1):
                    st.write(f"{i}. {url}")
                    
            except Exception as e:
                st.error(f"❌ Error searching Google: {str(e)}")
        else:
            st.warning("⚠️ Please enter a search query")
    
    st.subheader("🕷️ Web Scraping")
    
    url_to_scrape = st.text_input("URL to Scrape:")
    
    if st.button("🕷️ Scrape Website"):
        if url_to_scrape:
            try:
                response = requests.get(url_to_scrape)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                text_content = soup.get_text()
                
                links = soup.find_all('a')
                link_urls = [link.get('href') for link in links if link.get('href')]
                
                images = soup.find_all('img')
                image_urls = [img.get('src') for img in images if img.get('src')]
                
                st.write("**Scraped Content:**")
                st.write(f"**Text Length:** {len(text_content)} characters")
                st.write(f"**Number of Links:** {len(link_urls)}")
                st.write(f"**Number of Images:** {len(image_urls)}")
                
                st.text_area("Text Preview:", text_content[:500] + "..." if len(text_content) > 500 else text_content)
                
                if link_urls:
                    st.write("**Links:**")
                    for i, link in enumerate(link_urls[:10], 1):
                        st.write(f"{i}. {link}")
                
            except Exception as e:
                st.error(f"❌ Error scraping website: {str(e)}")
        else:
            st.warning("⚠️ Please enter a URL")
    
    st.subheader("📱 Social Media Posting")
    
    social_platform = st.selectbox("Select Platform:", ["Twitter", "Instagram", "Facebook"])
    post_content = st.text_area("Post Content:")
    
    if st.button("📱 Post to Social Media"):
        if post_content:
            try:
                if social_platform == "Twitter":
                    st.info("Twitter posting requires API keys. Please configure in the sidebar.")
                    
                elif social_platform == "Instagram":
                    st.info("Instagram posting requires API keys. Please configure in the sidebar.")
                    
                elif social_platform == "Facebook":
                    st.info("Facebook posting requires API keys. Please configure in the sidebar.")
                    
            except Exception as e:
                st.error(f"❌ Error posting to {social_platform}: {str(e)}")
        else:
            st.warning("⚠️ Please enter post content")

def show_media_graphics_tools():
    st.header("🎨 Media & Graphics Tools")
    
    st.subheader("🎨 Digital Image Creator")
    
    image_width = st.number_input("Image Width:", min_value=100, max_value=1920, value=800)
    image_height = st.number_input("Image Height:", min_value=100, max_value=1080, value=600)
    background_color = st.color_picker("Background Color:", "#ffffff")
    text_content = st.text_input("Text to Add:")
    text_color = st.color_picker("Text Color:", "#000000")
    
    if st.button("🎨 Create Digital Image"):
        try:
            img = Image.new('RGB', (image_width, image_height), background_color)
            draw = ImageDraw.Draw(img)
            
            if text_content:
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
                except:
                    font = ImageFont.load_default()
                
                bbox = draw.textbbox((0, 0), text_content, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                x = (image_width - text_width) // 2
                y = (image_height - text_height) // 2
                
                draw.text((x, y), text_content, fill=text_color, font=font)
            
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            st.image(img_bytes, caption="Generated Digital Image", use_column_width=True)
            
            st.download_button(
                label="💾 Download Image",
                data=img_bytes.getvalue(),
                file_name="digital_image.png",
                mime="image/png"
            )
        except Exception as e:
            st.error(f"❌ Error creating image: {str(e)}")
    
    st.subheader("🔄 Face Swapping")
    
    st.info("Face swapping requires advanced computer vision libraries. This is a placeholder for the functionality.")
    
    image1 = st.file_uploader("Upload First Image (Source):", type=['jpg', 'jpeg', 'png'])
    image2 = st.file_uploader("Upload Second Image (Target):", type=['jpg', 'jpeg', 'png'])
    
    if st.button("🔄 Swap Faces"):
        if image1 and image2:
            st.info("Face swapping functionality would be implemented here with OpenCV and face recognition libraries.")
        else:
            st.warning("⚠️ Please upload both images")

def show_ai_automation_tools():
    st.header("🤖 AI & Automation Tools")
    
    st.subheader("🤖 ChatGPT Integration")
    
    openai_api_key = st.text_input("OpenAI API Key:", type="password")
    chat_prompt = st.text_area("ChatGPT Prompt:")
    
    if st.button("🤖 Send to ChatGPT"):
        if openai_api_key and chat_prompt:
            try:
                import openai
                openai.api_key = openai_api_key
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": chat_prompt}
                    ]
                )
                
                st.write("**ChatGPT Response:**")
                st.write(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"❌ Error with ChatGPT: {str(e)}")
        else:
            st.warning("⚠️ Please enter API key and prompt")
    
    st.subheader("🎨 AI Image Generation")
    
    image_prompt = st.text_area("Image Generation Prompt:")
    
    if st.button("🎨 Generate Image"):
        if image_prompt:
            try:
                import openai
                
                if openai_api_key:
                    openai.api_key = openai_api_key
                    
                    response = openai.Image.create(
                        prompt=image_prompt,
                        n=1,
                        size="1024x1024"
                    )
                    
                    image_url = response['data'][0]['url']
                    st.image(image_url, caption="Generated Image", use_column_width=True)
                    
                else:
                    st.warning("⚠️ Please enter OpenAI API key")
                    
            except Exception as e:
                st.error(f"❌ Error generating image: {str(e)}")
        else:
            st.warning("⚠️ Please enter an image prompt")
    
    st.subheader("🎤 Voice Recognition")
    
    st.info("Voice recognition functionality would be implemented here with speech recognition libraries.")
    
    audio_file = st.file_uploader("Upload Audio File:", type=['wav', 'mp3'])
    
    if st.button("🎤 Transcribe Audio"):
        if audio_file:
            st.info("Audio transcription would be implemented here with speech recognition libraries.")
        else:
            st.warning("⚠️ Please upload an audio file")
