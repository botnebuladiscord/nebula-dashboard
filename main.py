from flask import Flask, render_template, request, session, redirect
from zenora import APIClient
import os
import requests
import json

app = Flask('Nebula - Dashboard', template_folder='templates')

key = os.environ.get('KEY')
redirect_url = os.environ.get('REDIRECT')
url = os.environ.get('AUTHURL')
url = url.replace('{redirect_url}', redirect_url)
token = os.environ.get('TOKEN')
secret = os.environ.get('SECRET')
client = APIClient(token, client_secret=secret)
bot_id = 953533453100527626
updates_channel = 873941729219338311

app.config['SECRET_KEY'] = 'session'

@app.route('/')
@app.route('/home')
def home():
    current_user = False
    if 'user' in session:
        try:
            user = APIClient(session.get('user'), bearer=True)
            serversraw = user.users.get_my_guilds()
            token = os.environ.get('TOKEN')
            header = {'Authorization':'Bot '+token}
            guilds = requests.get('https://discord.com/api/v10/users/@me/guilds', headers=header).json()
            guildse = []
            servers = []
            for i in guilds:
                guildse.append(i['id'])
            for server in serversraw:
                if str(server.id) in guildse:
                    servers.append(server)
            session['servers'] = guildse
            user = user.users.get_current_user()
            current_user = True
            avatar = user.avatar_url
            name = user.username
        except:
            avatar = None
            name = None
            servers = []
    else:
        avatar = None
        name = None
        servers = []
    return render_template('/home.html', key=key, url=url, current_user=current_user, avatar=avatar, name=name, servers=servers)

@app.route('/callback')
def callback():
    try:
        code = request.values['code']
        access_token = client.oauth.get_access_token(code, redirect_url).access_token
        session['user'] = access_token
    except:
        pass
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/manage/<serverid>')
def manage_overview(serverid):
    servers = session.get('servers')
    try:
        user = APIClient(session.get('user'), bearer=True).users.get_current_user().id
        server = None
        if str(serverid) in servers:
            token = os.environ.get('TOKEN')
            header = {'Authorization':'Bot '+token}
            guild = requests.get(f'https://discord.com/api/v10/guilds/{serverid}', headers=header).json()
            channels = requests.get(f'https://discord.com/api/v10/guilds/{serverid}/channels', headers=header).json()
            rolesraw = guild['roles']
            roles = []
            for i in rolesraw:
                if int(i['permissions']) & 0x8 == 0x8 or int(i['permissions']) & 0x20 == 0x20:
                    if i['name'] == '@everyone':
                        server = guild
                    roles.append(i['id'])
            user = requests.get(f'https://discord.com/api/v10/guilds/{serverid}/members/{user}', headers=header).json()
            for i in user['roles']:
                if i in roles:
                    server = guild
                    break    
            else:
                if int(guild['owner_id']) == int(user['user']['id']):
                    server = guild
            me = requests.get(f'https://discord.com/api/v10/guilds/{serverid}/members/{bot_id}', headers=header).json()
    except:
        server = None
        return render_template('/manage.html', server=server)
    if server == None:
        return render_template('/manage.html', server=server)
    session['current_server'] = server['id']
    return render_template('/manage.html', server=server, channels=channels, me=me)

@app.route('/manage/<serverid>/commands')
def manage_commands(serverid):
    servers = session.get('servers')
    try:
        user = APIClient(session.get('user'), bearer=True).users.get_current_user().id
        server = None
        if str(serverid) in servers:
            token = os.environ.get('TOKEN')
            header = {'Authorization':'Bot '+token}
            guild = requests.get(f'https://discord.com/api/v10/guilds/{serverid}', headers=header).json()
            permissions = requests.get(f'https://discord.com/api/v10/applications/{bot_id}/guilds/{serverid}/commands/permissions', headers=header).json()
            channels = requests.get(f'https://discord.com/api/v10/guilds/{serverid}/channels', headers=header).json()
            rolesraw = guild['roles']
            roles = []
            for i in rolesraw:
                if int(i['permissions']) & 0x8 == 0x8 or int(i['permissions']) & 0x20 == 0x20:
                    if i['name'] == '@everyone':
                        server = guild
                    roles.append(i['id'])
            user = requests.get(f'https://discord.com/api/v10/guilds/{serverid}/members/{user}', headers=header).json()
            for i in user['roles']:
                if i in roles:
                    server = guild
                    break    
            else:
                if int(guild['owner_id']) == int(user['user']['id']):
                    server = guild
            me = requests.get(f'https://discord.com/api/v10/guilds/{serverid}/members/{bot_id}', headers=header).json()
    except:
        server = None
        return render_template('/commands.html', server=server)
    if server == None:
        return render_template('/manage.html', server=server)
    session['current_server'] = server['id']
    commandsraw = requests.get(f'https://discord.com/api/v10/applications/{bot_id}/commands', headers=header)
    commandsraw = commandsraw.json()
    commands = {}
    for i in commandsraw:
        if i['name'] != 'help' and i['name'] != 'getmoney':
            for j in permissions:
                if i['id'] == j['id']:
                    for k in j['permissions']:
                        if k['id'] == str(serverid):
                            perm = k['permission']
                            commands[i['name']] = {'d':i['description'], 'p':perm}
                            break
            else:
                commands[i['name']] = {'d':i['description'], 'p':True}
    return render_template('/commands.html', server=server, channels=channels, me=me, commands=commands)

@app.route('/change_verification_level/<val>')
def change_verification_level(val):
    servers = session.get('servers')
    serverid = session.get('current_server')
    try:
        user = APIClient(session.get('user'), bearer=True).users.get_current_user().id
        server = None
        if str(serverid) in servers:
            token = os.environ.get('TOKEN')
            header = {'Authorization':'Bot '+token}
            guild = requests.get(f'https://discord.com/api/v10/guilds/{serverid}', headers=header).json()
            rolesraw = guild['roles']
            roles = []
            for i in rolesraw:
                if int(i['permissions']) & 0x8 == 0x8 or int(i['permissions']) & 0x20 == 0x20:
                    if i['name'] == '@everyone':
                        server = guild
                    roles.append(i['id'])
            user = requests.get(f'https://discord.com/api/v10/guilds/{serverid}/members/{user}', headers=header).json()
            for i in user['roles']:
                if i in roles:
                    server = guild
                    break    
            else:
                if int(guild['owner_id']) == int(user['user']['id']):
                    server = guild
    except:
        server = None
    if server == None:
        return "Unauthorized"
    header = {'Authorization':'Bot '+token, 'Content-Type': 'application/json'}
    val = str(val).replace(' ', '_')
    requests.patch(f'https://discord.com/api/v10/guilds/{serverid}', headers=header, json={'verification_level': int(val)}).text
    return ('None')

@app.route('/change_bot_nickname/<nickname>')
def change_bot_nickname(nickname):
    servers = session.get('servers')
    serverid = session.get('current_server')
    try:
        user = APIClient(session.get('user'), bearer=True).users.get_current_user().id
        server = None
        if str(serverid) in servers:
            token = os.environ.get('TOKEN')
            header = {'Authorization':'Bot '+token}
            guild = requests.get(f'https://discord.com/api/v10/guilds/{serverid}', headers=header).json()
            rolesraw = guild['roles']
            roles = []
            for i in rolesraw:
                if int(i['permissions']) & 0x8 == 0x8 or int(i['permissions']) & 0x20 == 0x20:
                    if i['name'] == '@everyone':
                        server = guild
                    roles.append(i['id'])
            user = requests.get(f'https://discord.com/api/v10/guilds/{serverid}/members/{user}', headers=header).json()
            for i in user['roles']:
                if i in roles:
                    server = guild
                    break    
            else:
                if int(guild['owner_id']) == int(user['user']['id']):
                    server = guild
    except:
        server = None
    if server == None:
        return "Unauthorized"
    header = {'Authorization':'Bot '+token, 'Content-Type': 'application/json'}
    if nickname == 'n':
        nickname = None
    requests.patch(f'https://discord.com/api/v10/guilds/{serverid}/members/@me', headers=header, json={'nick': nickname}).text
    return ('None')

@app.route('/change_updates_channel/<val>')
def change_updates_channel(val):
    servers = session.get('servers')
    serverid = session.get('current_server')
    try:
        user = APIClient(session.get('user'), bearer=True).users.get_current_user().id
        server = None
        if str(serverid) in servers:
            token = os.environ.get('TOKEN')
            header = {'Authorization':'Bot '+token}
            guild = requests.get(f'https://discord.com/api/v10/guilds/{serverid}', headers=header).json()
            rolesraw = guild['roles']
            roles = []
            for i in rolesraw:
                if int(i['permissions']) & 0x8 == 0x8 or int(i['permissions']) & 0x20 == 0x20:
                    if i['name'] == '@everyone':
                        server = guild
                    roles.append(i['id'])
            user = requests.get(f'https://discord.com/api/v10/guilds/{serverid}/members/{user}', headers=header).json()
            for i in user['roles']:
                if i in roles:
                    server = guild
                    break    
            else:
                if int(guild['owner_id']) == int(user['user']['id']):
                    server = guild
    except:
        server = None
    if server == None:
        return "Unauthorized"
    header = {'Authorization':'Bot '+token, 'Content-Type': 'application/json'}
    requests.post(f'https://discord.com/api/v10/channels/{updates_channel}/followers', headers=header, json={'webhook_channel_id': val})
    return ('None')

@app.route('/change_command_status_d/<val>')
def change_command_status_d(val):
    acc_token = session.get('user')
    serverid = session.get('current_server')
    servers = session.get('servers')
    if str(serverid) in servers:
        header = {'Authorization':'Bot '+token, 'Content-Type': 'application/json'}
        commands = requests.get(f'https://discord.com/api/v10/applications/{bot_id}/commands', headers=header)
        commands = commands.json()
        for i in commands:
            if i['name'] == val:
                command = i['id']
        data = {'id': serverid, 'type': 1, 'permission': False}
        header = {'Authorization':'Bearer '+acc_token, 'Content-Type': 'application/json'}
        commands = requests.put(f'https://discord.com/api/v10/applications/{bot_id}/guilds/{serverid}/commands/{command}/permissions', headers=header, json={'permissions':[data]})
    return ('None')

@app.route('/change_command_status_e/<val>')
def change_command_status_e(val):
    serverid = session.get('current_server')
    acc_token = session.get('user')
    servers = session.get('servers')
    if str(serverid) in servers:
        header = {'Authorization':'Bot '+token, 'Content-Type': 'application/json'}
        commands = requests.get(f'https://discord.com/api/v10/applications/{bot_id}/commands', headers=header)
        commands = commands.json()
        for i in commands:
            if i['name'] == val:
                command = i['id']
        data = {'id': serverid, 'type': 1, 'permission': True}
        header = {'Authorization':'Bearer '+acc_token, 'Content-Type': 'application/json'}
        commands = requests.put(f'https://discord.com/api/v10/applications/{bot_id}/guilds/{serverid}/commands/{command}/permissions', headers=header, json={'permissions':[data]})
        return ('None')

@app.route('/manage/<serverid>/roles')
def manage_roles(serverid):
    servers = session.get('servers')
    try:
        user = APIClient(session.get('user'), bearer=True).users.get_current_user().id
        server = None
        if str(serverid) in servers:
            token = os.environ.get('TOKEN')
            header = {'Authorization':'Bot '+token}
            guild = requests.get(f'https://discord.com/api/v10/guilds/{serverid}', headers=header).json()
            rolesraw = guild['roles']
            roles = []
            for i in rolesraw:
                if int(i['permissions']) & 0x8 == 0x8 or int(i['permissions']) & 0x20 == 0x20:
                    if i['name'] == '@everyone':
                        server = guild
                    roles.append(i['id'])
            user = requests.get(f'https://discord.com/api/v10/guilds/{serverid}/members/{user}', headers=header).json()
            for i in user['roles']:
                if i in roles:
                    server = guild
                    break    
            else:
                if int(guild['owner_id']) == int(user['user']['id']):
                    server = guild
            me = requests.get(f'https://discord.com/api/v10/guilds/{serverid}/members/{bot_id}', headers=header).json()
    except:
        server = None
        return render_template('/roles.html', server=server)
    if server == None:
        return render_template('/manage.html', server=server)
    session['current_server'] = server['id']
    for i in rolesraw:
        if i['color'] != 0:
            i['color'] = str(hex(i['color'])).replace('0x', '')
        else:
            i['color'] = "99AAB5"
    commandsraw = requests.get(f'https://discord.com/api/v10/applications/{bot_id}/commands', headers=header)
    commandsraw = commandsraw.json()
    commands = {}
    roleperms = {}
    permissions = requests.get(f'https://discord.com/api/v10/applications/{bot_id}/guilds/{serverid}/commands/permissions', headers=header).json()
    for i in commandsraw:
        if i['name'] != 'help' and i['name'] != 'getmoney':
            commands[i['name']] = {'d':i['description']}
    for role in rolesraw:
        perms = ''
        for i in commandsraw:
            if i['name'] != 'help' and i['name'] != 'getmoney':
                for j in permissions:
                    if j['id'] != str(bot_id) and j['id'] == i['id']:
                        for k in j['permissions']:
                            if k['id'] != str(serverid):
                                cmdsselect = ''
                                for l in commandsraw:
                                    if i['name'] != 'help' and i['name'] != 'getmoney' and i['name'] == l['name']:
                                        cmdsselect+= f'<option value="{l["name"]}" selected>{l["name"]}</option>'
                                    elif i['name'] != 'help' and i['name'] != 'getmoney':
                                        cmdsselect += f'<option value="{l["name"]}">{l["name"]}</option>'
                                if k['id'] == role['id']:
                                    if k['permission']:
                                        perms += f'<div id="permission"><select id="commands-select" class="commands-select">{cmdsselect}</select><button class="rulebtn" style="background-color:#28A745;"></button><ion-icon id="delrule" class="delrule" name="trash"></ion-icon></div>'
                                    else:
                                        perms += f'<div id="permission"><select id="commands-select" class="commands-select">{cmdsselect}</select><button class="rulebtn" style="background-color:red;"></button><ion-icon id="delrule" class="delrule" name="trash"></ion-icon></div>'
                        roleperms[role['name']] = perms
                        break
        if perms != '':
            roleperms[role['name']] = perms
        else:
            roleperms[role['name']] = None
    return render_template('/roles.html', server=server, me=me, roles=rolesraw, commands=commands, roleperms=roleperms)

@app.route('/change_role_color/<roleid>/<color>')
def change_role_color(roleid, color):
    serverid = session.get('current_server')
    servers = session.get('servers')
    if str(serverid) in servers:
        header = {'Authorization':'Bot '+token, 'Content-Type': 'application/json'}
        response = requests.patch(f'https://discord.com/api/v10//guilds/{serverid}/roles/{roleid}', headers=header, json={'color':int(color, 16)})
        return {'status': response.status_code}

@app.route('/set_role_name/<roleid>/<rolename>')
def change_role_name(roleid, rolename):
    serverid = session.get('current_server')
    servers = session.get('servers')
    if str(serverid) in servers:
        header = {'Authorization':'Bot '+token, 'Content-Type': 'application/json'}
        response = requests.patch(f'https://discord.com/api/v10//guilds/{serverid}/roles/{roleid}', headers=header, json={'name':rolename})
        return {'status': response.status_code}

@app.route('/change_role_status_e/<cmd>/<roleid>')
def change_role_status_e(cmd, roleid):
    serverid = session.get('current_server')
    acc_token = session.get('user')
    servers = session.get('servers')
    if str(serverid) in servers:
        header = {'Authorization':'Bot '+token, 'Content-Type': 'application/json'}
        commands = requests.get(f'https://discord.com/api/v10/applications/{bot_id}/commands', headers=header)
        commands = commands.json()
        for i in commands:
            if i['name'] == cmd:
                command = i['id']
        perms = requests.get(f'https://discord.com/api/v10/applications/{bot_id}/guilds/{serverid}/commands/{command}/permissions', headers=header).json()
        try:
            data = list(perms['permissions'])
            data.append({'id': roleid, 'type': 1, 'permission': True})
        except:
            data = [{'id': roleid, 'type': 1, 'permission': True}]
        header = {'Authorization':'Bearer '+acc_token, 'Content-Type': 'application/json'}
        response = requests.put(f'https://discord.com/api/v10/applications/{bot_id}/guilds/{serverid}/commands/{command}/permissions', headers=header, json={'permissions':data})
        return {'status': response.status_code} 
    
@app.route('/change_role_status_del/<cmd>/<roleid>')
def change_role_status_del(cmd, roleid):
    serverid = session.get('current_server')
    acc_token = session.get('user')
    servers = session.get('servers')
    if str(serverid) in servers:
        header = {'Authorization':'Bot '+token, 'Content-Type': 'application/json'}
        commands = requests.get(f'https://discord.com/api/v10/applications/{bot_id}/commands', headers=header)
        commands = commands.json()
        for i in commands:
            if i['name'] == cmd:
                command = i['id']
        perms = requests.get(f'https://discord.com/api/v10/applications/{bot_id}/guilds/{serverid}/commands/{command}/permissions', headers=header).json()

        data = list(perms['permissions'])
        data.pop(data.index({'id': roleid, 'type': 1, 'permission': True}))

        header = {'Authorization':'Bearer '+acc_token, 'Content-Type': 'application/json'}
        response = requests.put(f'https://discord.com/api/v10/applications/{bot_id}/guilds/{serverid}/commands/{command}/permissions', headers=header, json={'permissions':data})
        return {'status': response.status_code} 

@app.route('/change_role_status_d/<cmd>/<roleid>')
def change_role_status_d(cmd, roleid):
    serverid = session.get('current_server')
    acc_token = session.get('user')
    servers = session.get('servers')
    if str(serverid) in servers:
        header = {'Authorization':'Bot '+token, 'Content-Type': 'application/json'}
        commands = requests.get(f'https://discord.com/api/v10/applications/{bot_id}/commands', headers=header)
        commands = commands.json()
        for i in commands:
            if i['name'] == cmd:
                command = i['id']
        perms = requests.get(f'https://discord.com/api/v10/applications/{bot_id}/guilds/{serverid}/commands/{command}/permissions', headers=header).json()
        try:
            data = list(perms['permissions'])
            data.append({'id': roleid, 'type': 1, 'permission': False})
        except:
            data = [{'id': roleid, 'type': 1, 'permission': False}]
        header = {'Authorization':'Bearer '+acc_token, 'Content-Type': 'application/json'}
        response = requests.put(f'https://discord.com/api/v10/applications/{bot_id}/guilds/{serverid}/commands/{command}/permissions', headers=header, json={'permissions':data})
        return {'status': response.status_code}

@app.route('/manage/<serverid>/emojis')
def manage_emojis(serverid):
    servers = session.get('servers')
    try:
        user = APIClient(session.get('user'), bearer=True).users.get_current_user().id
        server = None
        if str(serverid) in servers:
            token = os.environ.get('TOKEN')
            header = {'Authorization':'Bot '+token}
            guild = requests.get(f'https://discord.com/api/v10/guilds/{serverid}', headers=header).json()
            rolesraw = guild['roles']
            roles = []
            for i in rolesraw:
                if int(i['permissions']) & 0x8 == 0x8 or int(i['permissions']) & 0x20 == 0x20:
                    if i['name'] == '@everyone':
                        server = guild
                    roles.append(i['id'])
            user = requests.get(f'https://discord.com/api/v10/guilds/{serverid}/members/{user}', headers=header).json()
            for i in user['roles']:
                if i in roles:
                    server = guild
                    break    
            else:
                if int(guild['owner_id']) == int(user['user']['id']):
                    server = guild
            me = requests.get(f'https://discord.com/api/v10/guilds/{serverid}/members/{bot_id}', headers=header).json()
    except:
        server = None
        return render_template('/emojis.html', server=server)
    if server == None:
        return render_template('/emojis.html', server=server)
    session['current_server'] = server['id']
    
    return render_template('/emojis.html', server=server, me=me, emojis=guild['emojis'])
        

app.run(host='0.0.0.0', port=1000, debug=True)
