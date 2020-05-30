#!/usr/bin/env python3

from os.path import expanduser

from socket import \
    socket as sock, \
    timeout as TimeOutError, \
    SOCK_DGRAM, SHUT_WR, \
    AF_INET, SOCK_STREAM

from yaml import load as yload, Loader

from argparse import ArgumentParser

from time import sleep

try:
    import readline
except ModuleNotFoundError:
    pass

import requests

import inquirer

import cmd

class PylovCLI(cmd.Cmd):
	servers = {}
	socket = sock(AF_INET, SOCK_STREAM)
	gameini = ''
	itemtbl = ''
	maps = {}
	srv = None
	def __init__(self, *args, **kwargs):
		self.use_rawinput = False
		for (k, v) in kwargs.items():
			if hasattr(self, k):
				setattr(self, k, v)
		super().__init__()
		try:
			self.serverselect()
		except IndexError as err:
			print('known index error occured, restarting')
			self.serverselect()
	

	def serverselect(self):
		
		if not self.srv:
			self.srv = self._login()
		#print(self.servers)
		cmd = self._cmdselects()
		if cmd is None:
			return self.serverselect()
		res = self.fire(cmd)
		if res:
			print(res)
		print(cmd)
		if cmd == 'Disconnect':
			self.socket.close()
			self.srv = None
			self.maps = {}
			self.socket = sock(AF_INET, SOCK_STREAM)
		self.serverselect()

	def _login(self):
		"""server login method"""
		ask = [
			inquirer.List(
				'srv',
				message='select server',
				choices=[s for s in self.servers.keys()] + ['Exit'],
			),
		]
		srv = list(inquirer.prompt(ask).values())[0]
		if srv == 'Exit':
			exit()
		passwd = self.servers[srv][0]
		if len(self.servers[srv]) > 1:
			maplist = self.servers[srv][1]
		server, port = srv.split(':')
		self.socket.connect((server, int(port)))
		self._send('')
		print(self._send(passwd))
		return srv
		#self.prompt = '%s:%s >'%(server, port)

	def _getmapname(self, mapid):
		url = 'https://steamcommunity.com/sharedfiles/filedetails/?id='
		res = requests.post('%s%s'%(url, mapid.strip('UGC')))
		for l in res.text.split('\n'):
			if 'workshopItemTitle' in l:
				return l.split('>')[1].split('<')[0]

	def _getmaps(self):
		maplst = self.gameini
		if len(self.servers[self.srv]) > 1:
			maplst = self.servers[self.srv][1]
		if maplst.startswith('~'):
			maplst = expanduser(maplst)
		if not maplst.startswith('/'):
			print('error: cannot read maplist if no absolute path is provided')
		with open(maplst, 'r') as mfh:
			lines = mfh.readlines()
		if not self.maps:
			print('receiving map names - depending on the size of your maplist this can take a while (needed once per server usage)...')
			for l in lines:
				if not l or not l.startswith('MapRotation'):
					continue
				ugcid = l.split('MapId="')[1].split('", ')[0]
				gmmod = l.split('GameMode="')[1].split('")')[0]
				name = self._getmapname(ugcid)
				self.maps[name] = [ugcid, gmmod]
		ask = [
			inquirer.List(
				'map',
				carousel=True,
				message='select map',
				choices=[m for m in self.maps.keys()],
			),
		]
		mapp = list(inquirer.prompt(ask).values())[0]
		mmod = self.maps[mapp][1]
		modes = [mmod] + [s for s in ['SND', 'TDM', 'DM', 'GUN'] if s != mmod]
		ask = [
			inquirer.List(
				'mod',
				carousel=True,
				message='select mode (irrelevant if set by map)',
				choices=[m for m in modes],
			),
		]
		mode = list(inquirer.prompt(ask).values())[0]
		return '%s %s'%(self.maps[mapp][0], mode)

	def _getitem(self):
		with open(self.itemtbl, 'r') as ifh:
			items = [l.split(',')[0] for l in ifh.readlines()]
		ask = [
			inquirer.List(
				'item',
				carousel=True,
				message='select item',
				choices=items,
			),
		]
		return list(inquirer.prompt(ask).values())[0]


	def _getskin(self):
		ask = [
			inquirer.List(
				'skin',
				carousel=True,
				message='select skin',
				choices=['clown', 'prisoner', 'naked', 'farmer', 'russian', 'nato'],
			),
		]
		return list(inquirer.prompt(ask).values())[0]

	def _getammotype(self):
		ask = [
			inquirer.List(
				'ammo',
				carousel=True,
				message='select ammo-limit',
				choices=[0, 1, 2],
			),
		]
		return list(inquirer.prompt(ask).values())[0]

	def _getteam(self):
		ask = [
			inquirer.List(
				'team',
				carousel=True,
				message='select team',
				choices=["Blue Team (Defenders)", "Red Team (Attackers)"],
			),
		]
		return list(inquirer.prompt(ask).values())[0]

	def _getcash(self):
		c = 0
		while True:
			cash = input('enter amount of cash (as number)')
			if cash.isdigit():
				return cash
			c+=1
			if c < 3:
				print('thats not a number - let\'s try again')
			else:
				print('too dumb for numbers? o.0 aborting...')
			
	def _cmdselects(self):
		noargs = ['ResetSND', 'RefreshList', 'RotateMap', 'ServerInfo', 'Help', 'Disconnect']
		steams = ['Kick', 'Ban', 'Unban', 'InspectPlayer']
		others = ['SwitchMap', 'SwitchTeam', 'GiveItem', 'GiveCash', 'GiveTeamCash', 'SetPlayerSkin', 'SetLimitedAmmoType']
		hlp = self._send('Help')
		#print(hlp)
		hlp = hlp.strip().strip('{}').split('": "')[1].strip().rstrip('"')
		hlp = [h.split(' ')[0] for h in hlp.split(', ')]
		ask = [
			inquirer.List(
				'cmd',
				carousel=True,
				message='select command',
				choices=hlp,
			),
		]
		cmd = list(inquirer.prompt(ask).values())[0].strip()
		if cmd in noargs:
			return cmd
		elif cmd in steams:
			sid = self._getsteamid(cmd)
			if not sid:
				return
			return '%s %s'%(cmd, sid)
		elif cmd in others:
			if cmd == 'SwitchMap':
				return 'SwitchMap %s'%self._getmaps()
			elif cmd == 'SwitchTeam':
				sid = self._getsteamid(cmd)
				if not sid:
					return
				return 'SwitchTeam %s %s'%(sid, self._getteam())
			elif cmd == 'GiveItem':
				sid = self._getsteamid(cmd)
				if not sid:
					return
				return 'GiveItem %s %s'%(sid, self._getitem())
			elif cmd == 'GiveCash':
				sid = self._getsteamid(cmd)
				if not sid:
					return
				return 'GiveCash %s %s'%(sid, self._getcash())
			elif cmd == 'GiveTeamCash':
				return 'GiveTeamCash %s %s'%(self._getteam(), self._getcash())
			elif cmd == 'SetPlayerSkin':
				sid = self._getsteamid(cmd)
				if not sid:
					return
				return 'SetPlayerSkin %s %s'%(sid, self._getskin())
			elif cmd == 'SetLimitedAmmoType':
				return 'SetLimitedAmmoType %s'%self._getammotype()
				

	def _getsteamid(self, cmd):
		userids = self._players()
		if not userids:
			print('error: executing "%s" is impossible - no players\n\n'%cmd)
			sleep(2)
			return
		ask = [
			inquirer.List(
				'user',
				carousel=True,
				message='select user to %s'%cmd,
				choices=userids.keys(),
			),
		]
		return userids[inquirer.prompt(ask).values()[0]]

	def fire(self, cmd):
		res = self._send(cmd)
		if res:
			print(res)

	def _players(self):
		pout = self._send('RefreshList')
		pout = pout.split('{\n\t"PlayerList": [')[1]
		pout = pout.split('\t]\n}')[0]
		#print(pout)
		_players = {}
		for blk in pout.split('}'):
			useruid = [l.strip() for l in blk.rstrip('}').split('\n') if l.strip() and l.strip() not in (',', '{')]
			if not useruid or str(useruid).strip() == '[\']\']': continue
			print(useruid)
			_players[useruid[0].split('": "')[1].rstrip('",')] = useruid[1].split('": "')[1].rstrip('"')
		return _players

	def _send(self, data, answer=True):
		self.socket.sendall(data.encode())
		if answer:
			return self.socket.recv(1024).decode()

	#def default(self, line):
	#	if line == 'Disconnect':
	#		self.socket.close()
	#		self._login()
	#	else:
	#		out = self._send(line)


def cli(settings={}):
	with open(expanduser('~/.config/pavlovadm/pavlovadm.conf'), 'r') as cfh:
		configs = yload(cfh.read(), Loader=Loader)
	app = PylovCLI(**configs)
	app.cmdloop()









if __name__ == '__main__':
	cli()
