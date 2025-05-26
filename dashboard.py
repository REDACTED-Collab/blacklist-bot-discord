from quart import Quart, render_template, request, redirect, url_for, session, flash, jsonify
import json
import datetime
import os
import logging
import asyncio
from functools import wraps

app = Quart(__name__)

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

app.secret_key = config.get('dashboard', {}).get('secret', 'your-secret-key')
PORT = 8000  # Use port 8000 as specified

# Routes
@app.route('/')
async def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':
        form = await request.form
        username = form.get('username')
        password = form.get('password')
        
        # Check if user is a developer or has allowed role
        if username == 'admin' and password == config.get('dashboard', {}).get('secret', 'your-secret-key-change-this'):
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            await flash('Invalid credentials', 'danger')
    
    return await render_template('login.html')

@app.route('/dashboard')
async def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Get bot statistics
    uptime = str(datetime.datetime.now() - bot.start_time) if hasattr(bot, 'start_time') else 'N/A'
    stats = {
        'uptime': uptime,
        'total_blacklisted': len(bot.blacklist_data) if hasattr(bot, 'blacklist_data') else 0,
        'total_servers': len(bot.guilds) if hasattr(bot, 'guilds') else 0,
        'anti_evasion': config.get('anti_evasion', False)
    }
    
    # Get recent blacklist activity
    recent_activity = []
    try:
        with open('blacklist.log', 'r') as f:
            logs = f.readlines()[-10:]  # Get last 10 entries
            for log in logs:
                if 'BLACKLIST' in log:
                    parts = log.split(' - ')
                    if len(parts) >= 3:
                        timestamp = parts[0]
                        action_parts = parts[2].split(': ')
                        if len(action_parts) >= 2:
                            action = action_parts[0]
                            reason = action_parts[1].strip()
                            user = action_parts[0].split()[0]
                            recent_activity.append({
                                'user': user,
                                'action': action,
                                'reason': reason,
                                'date': timestamp
                            })
    except Exception as e:
        logging.error(f"Error reading blacklist activity: {e}")
    
    return await render_template('dashboard.html', stats=stats, recent_activity=recent_activity)

@app.route('/blacklist')
async def blacklist():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    blacklisted_users = []
    if hasattr(bot, 'blacklist_data'):
        for user_id, data in bot.blacklist_data.items():
            blacklisted_users.append({
                'user_id': user_id,
                'reason': data.get('reason', 'No reason provided'),
                'added_by': data.get('added_by', 'Unknown'),
                'added_at': data.get('added_at', 'Unknown')
            })
    
    return await render_template('blacklist.html', blacklisted_users=blacklisted_users)

@app.route('/logs')
async def logs():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    try:
        with open('blacklist.log', 'r') as f:
            logs = f.readlines()[-50:]  # Get last 50 lines
    except Exception as e:
        logs = [f"Error reading logs: {str(e)}"]
    
    return await render_template('logs.html', logs=logs)

@app.route('/api/toggle_anti_evasion', methods=['POST'])
async def toggle_anti_evasion():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        config['anti_evasion'] = not config.get('anti_evasion', False)
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        
        # Update bot's configuration
        if hasattr(bot, 'config'):
            bot.config['anti_evasion'] = config['anti_evasion']
            
        return jsonify({'status': 'success', 'anti_evasion': config['anti_evasion']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blacklist', methods=['GET'])
async def get_blacklist():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    try:
        blacklist = bot.blacklist_data if hasattr(bot, 'blacklist_data') else []
        return jsonify({'blacklist': blacklist})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blacklist/<user_id>', methods=['DELETE'])
async def remove_from_blacklist(user_id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    try:
        if hasattr(bot, 'remove_from_blacklist'):
            await bot.remove_from_blacklist(user_id, 'Removed via dashboard')
            return jsonify({'status': 'success'})
        return jsonify({'error': 'Bot not initialized'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

async def run_dashboard(bot_instance=None):
    global bot
    bot = bot_instance
    
    print(f"\n* Dashboard is available at http://localhost:{PORT}")
    
    # Run Quart app
    await app.run_task(host='0.0.0.0', port=PORT)

if __name__ == '__main__':
    run_dashboard()
