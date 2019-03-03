import discord
import asyncio
import datetime
import os
import random
import subprocess

client = discord.Client()
#discord.opus.load_opus

#to do:
#someBODy normal song, barney opening, The Bluest Star (song on repeat in tabletop simulator), Blend S OP beginning, HUAAAAA at the beginning of japan's hetalia ending, tabletop menu music
#fix changing game/time during tune play
#add cooldown
#add eyecatches, including Eiken's
#put Gilgamesh's quotes in a file

#variables, pretty self-explanatory
#date_time = date_time.now().hour
#time = date_time.now() #do not use: date_time.time() | can also try date_time.timestamp()
key = 0
game = 0
change = 0
slider = 0
nowP = 0
voice = ''
npGame = ''
npWeather = ''
gameAbv = ''
status = ''
realTime = ''
global tuneQ
tuneQ = 0
mother = '196692352478216193'
kanna = '358832138579345410'
mona = '210439640287543296'
gilgamesh = '356665027115089922'
general = discord.Object(196673593898303488)
anime = discord.Object(196820716748931072)
games = discord.Object(196829323561271297)
media = discord.Object(204441127607205889)
technology = discord.Object(285691200797802496)
art = discord.Object(292151521674788864)
shitposting = discord.Object(196772149766127616)
bot = discord.Object(197587968184025088)

#sets text to show what is now playing--is called when new song plays
async def setNP(sliderPlay):
	global nowP
	
	#sets nice game strings
	if slider == 0:
		if game == 0:
			npGame = 'Animal Crossing: New Leaf'
			gameAbv = 'New Leaf'
		elif game == 1:
			npGame = 'Animal Crossing: City Folk'
			gameAbv = 'City Folk'
		elif game == 3:
			npGame = 'GC Animal Crossing'
			gameAbv = 'Game Cube'
		
		#sets nice weather strings
		if key == 0:
			npWeather = 'Sun'
		elif key == 1:
			npWeather = 'Rain'
		elif key == 2:
			npWeather = 'Snow'
		
		#makes the time be 12-hour clock because we're shitty
		if tTime == 0:
			realTime = '12:00 AM'
		elif tTime < 12:
			realTime = str(tTime)+':00 AM'
		elif tTime == 12:
			realTime = '12:00 PM'
		elif tTime > 12:
			realTime = str(int(tTime) - 12)+':00 PM'
		
		#sets now playing string, abbreviated string for status
		nowP = 'Now Playing: '+'\n'+npGame+' | '+realTime+' | '+npWeather+' version'
		status = gameAbv+' | '+realTime+' | '+npWeather
		#await client.change_presence(game=discord.Game(name=status),afk=False)
	if slider == 1:
		nowP = 'Now Playing: '+sliderPlay
		status = sliderPlay
	await client.change_presence(game=discord.Game(name=status),afk=False)
		

# key:
# 0 is sun, 1 is rain, 2 is snow
def setKey(newKey):
	global key
	key = newKey
	setChange(1)
	
# game:
# 0 is acnl, 1 is accf, 2 is acww, 3 is acgc
def setGame(newGame):
	global game
	game = newGame
	setChange(1)

#allows bot to join VC
def setVoice(newVoice):
	global voice
	voice = newVoice
	
def setSlider(newslider):
	global slider
	slider = newslider
	setChange(1)

#to stop infinite recursion of Music(): if bot is told to =leave, it sets stop to 0, which tells Music() to return
def setChange(newchange):
	global change
	change = newchange

def setTime(newTime):
	global tTime
	if (int(newTime) <= 23) and (int(newTime) >=0):
		tTime = int(newTime)
		setChange(1)
	else:
		return True
	
async def displayTime(cTime, channel):
	icTime = int(cTime)
	if icTime == 0:
		await client.send_message(channel,"Time set to 12:00 AM.")
	elif (icTime > 11):
		if icTime == 12:
			aTime = icTime
		else:
			aTime = icTime - 12
		await client.send_message(channel,"Time set to %s:00 PM."%str(aTime))
	else:
		await client.send_message(channel,"Time set to %s:00 AM."%str(icTime))
		
	
def townTune():
	newTune = random.choice([x for x in os.listdir("tune/") if os.path.isfile(os.path.join("tune/", x))])
	return 'tune/'+newTune
	
def tuneQchange(integ):
	global tuneQ
	if (tuneQ + integ) > 6:
		tuneQ = 6
		print('tune queue limit exceeded')
	else:
		tuneQ = tuneQ + integ
	print('Tune queue: '+str(tuneQ))
	if tuneQ > 0:
		setChange(1)
	
	
async def playTune():
	#print('C o o l  V i b r a t i o n s')
	Tune = townTune()
	print(Tune)
	tuneplayer = voice.create_ffmpeg_player(Tune)
	tuneplayer.volume=0.5
	tuneplayer.start()
	while not tuneplayer.is_done():
		if change == 1:
			setChange(0)
			tuneplayer.stop()
		await asyncio.sleep(1)
	tuneplayer.stop()
	
async def reboot(message):
    await client.send_message(message.channel,'I will be right back, mother.')
    await client.logout()
    process = subprocess.Popen('Bot.bat', shell=True)

#plays music--sets now playing, starts player, waits until it's done or stops when told to leave,
#updates time and song, then calls itself with new song
async def Music(player):
	time = datetime.datetime.now().hour
	while not player.is_done(): #while player is playing
		if time != datetime.datetime.now().hour: #if the hour changed, update time and play town tune
			time = datetime.datetime.now().hour
			if tTime == 23:
				setTime(0)
			else:
				setTime(tTime + 1)
			player.stop()
			tuneQchange(1)
			await playTune()
			tuneQchange(-1)
			player.stop()
		if change == 1: #if game/time/weather was changed, stop song and start song with new settings
			setChange(0)
			player.stop()
			if tuneQ > 0:
				await playTune()
				tuneQchange(-1)
		await asyncio.sleep(1)
	player.stop()
	#await setNP(0)
	if slider == 0:
		newplayer = voice.create_ffmpeg_player('ac/'+str(game)+str(key)+str(tTime)+'ac.mp3')
		await setNP(0)
	elif slider == 1:
		kkSong = random.choice([x for x in os.listdir("slider/") if os.path.isfile(os.path.join("slider/", x))])
		newplayer = voice.create_ffmpeg_player('slider/'+kkSong)
		await setNP(kkSong)
	newplayer.volume=0.2
	newplayer.start()
	if player.is_playing() or newplayer.is_playing():
		await Music(newplayer)
	else:
		await client.change_presence(game=discord.Game(name='Animal Crossing'),afk=False)
		
#help menu in a fancy info box
async def getHelp(message):                                                                                            
	embed = discord.Embed(title="Commands:", description="", color=0xf9e063)
	embed.add_field(name="=join", value="joins vc", inline=True)
	embed.add_field(name="=leave", value="leaves vc", inline=True)
	embed.add_field(name="=game <par>", value="acnl, accf, acgc", inline=True)
	embed.add_field(name="=weather <par>", value="sun, rain, snow", inline=True)
	embed.add_field(name="=time <par>", value="[time], now", inline=True)
	embed.add_field(name="=kk", value="summons KK", inline=True)
	embed.add_field(name="=skip", value="skips KK song", inline=True)
	embed.add_field(name="=np", value="shows now playing", inline=True)
	embed.add_field(name="etc.", value="=tune, =hello", inline=True)
	await client.send_message(message.channel, embed=embed)
	
#gilgamesh saying random stuff
async def Say(diaset):
	say = random.choice(diaset)
	await client.send_message(bot, say)

@client.event
async def on_ready():
	print('\nReady!')
	#await client.send_message(discord.Object(id='356664185985433613'),'I am here to grace you all with my presence.')
	await client.change_presence(game=discord.Game(name='Animal Crossing'),afk=False)
	setTime(datetime.datetime.now().hour)
	setChange(0)
	
@client.event
async def on_message(message):
	#Gilgamesh responding
	if not message.content.startswith('=') and not message.content.startswith('$') and not message.content.startswith('.') and not message.content.startswith('t!') and not (gilgamesh in message.author.id):
		if 'Gilgamesh' in message.content or 'gilgamesh' in message.content:
			if kanna in message.author.id or mona in message.author.id:
				await client.send_message(bot,"You are not worthy of an audience with a king. Crawl back to your father's nest, mongrel.")
			elif mother not in message.author.id:
				dia = []
				dia.append("Mongrel, what did you just utter about the king of heroes?")
				dia.append("You'll regret saying that, peasant.")
				dia.append("Don't get cocky, mongrel.")
				dia.append("May your scattered remains entertain me, mongrel.")
				dia.append("I am the king of heroes. You, on the other hand, are nothing but a filthy, useless mongrel.")
				dia.append("The only hero in Heaven and Earth who is a real king is me. The rest are a collection of mongrels.")
				dia.append("Are you questioning me? A lowly mongrel questioning a king like me?")
				dia.append("I greant you the honor of my presence yet you can't recognize me; such ignorance isn't even worth living.")
				dia.append("You shall at least entertain me when you scatter away, mongrel.")
				dia.append("Do you want to die that badly, you cur?!")
				dia.append("You mongrel, I won't leave a single piece of your body!")
				dia.append("Damn fool... Are you trying to put me on the same ground as you, me who should be at the top?")
				
				await Say(dia)
			else:
				diame = []
				diame.append("Mother...")
				diame.append("Mother, please.")
				diame.append("Mother!")
				diame.append("You're a m-mongrel, mother! Wait, I'm sorry!")
				diame.append("Why are you talking about me, mother?")
				diame.append("Have you seen Kirei, mother?")
				diame.append("Do you need something, mother?")
				
				await Say(diame)
		elif 'Kirei' in message.content or 'kirei' in message.content:
			if kanna in message.author.id or mona in message.author.id:
				await client.send_message(bot,"You dare speak of my companion in that manner? There will be hell to pay for that statement--your father cannot save you now.")
			elif mother not in message.author.id:
				diak = []
				diak.append("Do not utter such words about my plaything.")
				
				await Say(diak)
			else:
				diakme = []
				diakme.append("Yes, mother, Kirei is doing well.")
				
				await Say(diakme)
	#hello!
	elif message.content.startswith('=hello'):
		print('Hello!')
		if message.author.id not in mother:
			await client.send_message(message.channel,'You have no right to talk to me, filthy mongrel.')
		else:
			await client.send_message(message.channel,'...hello, mother.')
	
	#change weather version of music:
	elif message.content.startswith('=weather'):
		cmdWeather = message.content.split(" ")
		if message.author.voice.voice_channel is None:
			await client.send_message(message.channel,'Join voice chat before you try to change the weather, filthy mongrel.')
		elif client.is_voice_connected(message.author.server) == False:
			await client.send_message(message.channel,'I am not connected to voice chat, mongrel.')
		elif slider == 1:
			await client.send_message(message.channel,'K.K. Slider is currently playing.')
		else:
			try:
				if "sun" in (cmdWeather[1]):
					if key == 0:
						await client.send_message(message.channel,'It is already sunny.')
					else:
						setKey(0)
						await client.send_message(message.channel,'It is sunny outside!')
				elif "rain" in (cmdWeather[1]):
					if game == 3:
						await client.send_message(message.channel,'No.')
					else:
						if key == 1:
							await client.send_message(message.channel,'It is already raining.')
						else:
							setKey(1)
							await client.send_message(message.channel,'It is raining outside!')
				elif "snow" in (cmdWeather[1]):
					if key == 2:
						await client.send_message(message.channel,'It is already snowing.')
					else:
						setKey(2)
						await client.send_message(message.channel,'It is snowing outside!')
			except:
				await client.send_message(message.channel,'Correct usage: =weather <par> | sun, rain, snow')
	
	#change game soundtrack is coming from:
	elif message.content.startswith('=game'):
		cmdGame = message.content.split(" ")
		if message.author.voice.voice_channel is None:
			await client.send_message(message.channel,'Join voice chat before you try to change the soundtrack, filthy mongrel.')
		elif client.is_voice_connected(message.author.server) == False:
			await client.send_message(message.channel,'I am not connected to voice chat, mongrel.')
		elif slider == 1:
			await client.send_message(message.channel,'K.K. Slider is currently playing.')
		else:
			try:
				if "acnl" in (cmdGame[1]):
					if game == 0:
						await client.send_message(message.channel,'Game is already Animal Crossing: New Leaf.')
					else:
						setGame(0)
						await client.send_message(message.channel,'Game set to Animal Crossing: New Leaf.')
				elif "accf" in (cmdGame[1]):
					if game == 1:
						await client.send_message(message.channel,'Game is already Animal Crossing: City Folk.')
					else:
						setGame(1)
						await client.send_message(message.channel,'Game set to Animal Crossing: City Folk.')
				elif "acww" in (cmdGame[1]):
					await client.send_message(message.channel,'I do not have the Animal Crossing: Wild World soundtrack. Go back to your hovel, mongrel.')
				elif "acgc" in (cmdGame[1]):
					if game == 3:
						await client.send_message(message.channel,'Game is already GC Animal Crossing.')
					else:
						setGame(3)
						await client.send_message(message.channel,'Game set to GC Animal Crossing.')
				elif "achhd" in (cmdGame[1]):
					await client.send_message(message.channel,'I do not have the Animal Crossing: Happy Home Designer soundtrack. Go back to your hovel, mongrel.')
				elif "acaf" in (cmdGame[1]):
					await client.send_message(message.channel,'That game never happened.')
			except:
				await client.send_message(message.channel,'Correct usage: =game <par> | acnl, accf')
				
	#test to see what various values are or something
	elif message.content.startswith('=test'):
		print("wat u doin")
	
	#logs bot out, only if you're me though
	elif message.content.startswith('=kill'):
		if message.author.id not in mother:
			await client.send_message(message.channel,'You dare attempt to kill me, the King of Heroes, mongrel?')
		else:
			await client.logout()
	
	#checks if already is in VC; if isn't, joins voice chat
	elif message.content.startswith('=join'):
		if client.is_voice_connected(message.author.server):
			await client.send_message(message.channel,'I am already connected to voice chat, mongrel.')
		else:
			if message.author.voice.voice_channel is None:
				await client.send_message(message.channel,'You are not connected to voice chat, mongrel.')
			else:
				setVoice(await client.join_voice_channel(message.author.voice.voice_channel))
				setTime(datetime.datetime.now().hour)
				setChange(0)
				player = voice.create_ffmpeg_player('ac/'+str(game)+str(key)+str(tTime)+'ac.mp3')
				player.volume=0.2
				await setNP(0)
				player.start()
				await Music(player)
	
	#stops music, disconnects from voice, changes status back to default
	elif message.content.startswith('=leave'):
		if client.is_voice_connected(message.author.server) == False:
			await client.send_message(message.channel,'I am not connected to voice chat, mongrel.')
		else:
			await voice.disconnect()
	
	#prints what is now playing into chat
	elif message.content.startswith('=np'):
		if client.is_voice_connected(message.author.server) == False:
			await client.send_message(message.channel,'I am not connected to voice chat, mongrel.')
		else:
			await client.send_message(message.channel,nowP)
		
	#changes time
	elif message.content.startswith('=time'):
		cmdTime = message.content.split(" ")
		if message.author.voice.voice_channel is None:
			await client.send_message(message.channel,'Join voice chat before you try to change the time, filthy mongrel.')
		elif client.is_voice_connected(message.author.server) == False:
			await client.send_message(message.channel,'I am not connected to voice chat, mongrel.')
		elif slider == 1:
			await client.send_message(message.channel,'K.K. Slider is currently playing.')
		else:
			try:
				if "now" in (cmdTime[1]):
					setTime(datetime.datetime.now().hour)
					await displayTime(datetime.datetime.now().hour, message.channel)
				elif setTime(cmdTime[1]) is True:
					await client.send_message(message.channel,"Not a valid time, mongrel.")
				else:
					setTime(cmdTime[1])
					await displayTime(cmdTime[1], message.channel)
			except:
				await client.send_message(message.channel,'Correct usage: =time <par> | 24-hour clock or "now"')
	
	#chooses a town tune
	elif message.content.startswith('=tune'):
		cmdTune = message.content.split(" ")
		if message.author.voice.voice_channel is None:
				await client.send_message(message.channel,"You do not have the right to assault others' ears without your ears being assaulted as well.")
		else:
			try:
				if "queue" in cmdTune[1]:
					await client.send_message(message.channel,"Tune queue: "+str(tuneQ - 1))
				elif (not cmdTune[1].isnumeric()) or (not ((int(cmdTune[1]) >0) and (int(cmdTune[1]) < 7))):
					await client.send_message(message.channel,"Invalid number of tunes. Peasant.")
				else:
					tuneQchange(int(cmdTune[1]))
			except:
				tuneQchange(1)
		
	#set K.K. Slider concert mode
	elif message.content.startswith('=kk'):
		if slider == 1:
			setSlider(0)
			await client.send_file(message.channel, 'kk leaving.png')
			await client.send_message(message.channel,'K.K. Slider is gone.')
		else:
			setSlider(1)
			await client.send_file(message.channel, 'kkimage/'+random.choice([x for x in os.listdir("kkimage/") if os.path.isfile(os.path.join("kkimage/", x))]))
			await client.send_message(message.channel,'K.K. Slider is here.')
		
	elif message.content.startswith('=skip'):
		if slider == 0:
			await client.send_message(message.channel,'K.K. Slider is not here, so you cannot skip songs.')
		else:
			setChange(1)
	
	elif message.content.startswith('=mongrel'): #make it do the mongrel tune
		await client.send_message(message.channel,'Zasshu!')
		
	elif message.content.startswith('=zasshu'):
		await client.send_message(message.channel,'Mongrel!')
		
	elif message.content.startswith('=lelf') or message.content.startswith('=eruerufu'):
		await client.send_message(message.channel,':rage: Eruerufu....')
	
	#elif message.content.startswith('=dildo'): make it play cool vibrations
		
	#restart the bot
	elif message.content.startswith('=reboot'):
		if message.author.id not in mother:
				await client.send_message(message.channel,'You dare attempt to reboot me, the King of Heroes, mongrel?')
		else:
			await reboot(message)
		
	elif message.content.startswith('=goodnight'):
		if mother in message.author.id:
			await client.send_message(message.channel,'...good night, mother.')
		else:
			await client.send_message(message.channel,'Fuck off, mongrel.')
		
	#lists (almost) all commands
	elif message.content.startswith('=ohelp'):
		await client.send_message(message.channel,'__**Help:**__\n**Voice:** =join, =leave\n**Change game:** =acnl, =accf\n**Change weather:** =sun, =rain, =snow\n**Change time:** =time [time] or =time now\n**etc:** =np, =hello, =test, =kill, =tune')
		
	#lists (almost) all commands
	elif message.content.startswith('=help'):
		await getHelp(message)
		
	
		
client.run('MzU2NjY1MDI3MTE1MDg5OTIy.DJep2g.MXQsawGvEqQ7j1GnfKx5z6KDYzw')