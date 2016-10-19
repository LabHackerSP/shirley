#!/usr/bin/python2
# coding: utf-8

from twx.botapi import TelegramBot, ReplyKeyboardMarkup
from subprocess import Popen, PIPE, STDOUT
from functools import partial
import re, datetime, random, time, codecs, pickle
from glob import glob
from markov import say, process

"""
Configurando o bot
"""

BOTAPI='247937795:AAHTtuvKV2a2pQF93wgDdVhWsK5IiNlCiAY'
bot = TelegramBot(BOTAPI)
bot.update_bot_info().wait()


ansi_escape = re.compile(r'\x1b[^m]+m')

molejo = """Acorda criancada ta na hora da gente brincar (oba)
Brincar de pique-esconde,pique-cola e de pique-ta, ta, ta, ta
Nessa brincadeira tambam tem pique-bandeira e amarelinha pra quem gosta de pular
E aquela brincadeira de beijar.
Eh essa ? nao,
Eh essa ? eh
Pera, uva, maca ou salada mista ?
Salada mista (beija beija)
Brincadeira de crianca
Como e bom, como e bom
Guardo ainda na lembranca
Paz, amor e esperanca
Diga aonde voce vai
Que eu vou varrendo
Vou varrendo, vou varrendo, vou varrendo, vou varrendo
Oh menininha eu sou seu fan
Danco contigo ate de manha
Na danca da bruxinha
Danca preta, danca loura
Agora todo mundo
Na dancinha da vassoura
Varre pra esquerda
Varre pra direita
Levanta poeira
Que essa danca eh porreta...
Piti pi piti pi piti pau!
Mas tome cuidado
Com o cabo da vassoura
Eh pior do que cenoura
Voce pode se dar mal..."""

funk = """é o pet é o pet
Na madruga boladona sentada na esquina
se ela dança eu danço
pra dançar créu tem que ter disposição
pra dançar créu tem que ter habilidade
traição é traição, romance é romance, amor é amor e um lance é um lance
Agora eu tô solteira e ninguém vai me segurar
Vem que vem que vem kicando
bota o dedinho na boca e faz cara de tarada
foge foge mulher maravilha foge com o super man
Eu vou pro baile procurar o meu negão
ela balança mas não pára
pra te enlouquecer todas que provaram não conseguem esquecer
Mas não se esqueça que eu sou vagabundo depois que a putaria começou rolar no mundo
Sou foda, Eu sou sinistro
Eu sou sinistro melhor que seu marido esculacho seu amigo no escuro eu sou um perigo
Faz quadradinho de 4
Papai jogo mel , e mamãe deu carinho , essa mulher , e pedaço de mal caminho
Ela desce ela kika , ela sobe ela empina
Olha os amigos lá em cima , jogando dinheiro do camarote
Bate o pé , treme a bunda e faz meu bonde passar mal
Ostentação fora do normal , quem tem moto faz amor e quem não tem passa mal
Garoto sem limite, se amarra em Red Bull com Whisky
Ela só pensa em beijar, beijar, beijar, beijar
Glamurosaaaaaa
Pre-pa-ra
To com o cu pegando fogo!
Beijinho no ombro pro recalque passar longe!"""


process(funk)
process(molejo)

print "started"

line = ""
title = "voltei"

bomdia = """DYA!
Bundinha!!
Bom dia :D
Dia !!! :)"""


perdi = """PERDI!!!!
hm... perdi !!!! :P
hehe, perdi
gente, PERDI!!!!!!!!!
peeeeeeerdi :)
p e r d i  :-X """

def chance(perc):
    return random.randint(0, 99) > (100 - perc)

def wrt(user,message):
    bot.send_message(user, message).wait()
    print 'Shirley: ' + message
    
def voice(m):
    pp = Popen(["espeak", "-vpt+f2", "'%s'" % m.replace("'", "'"), "-w", "/tmp/x.wav"], stdout=PIPE)
    pp.wait()
    pp = Popen(["rm", "-f", "/tmp/x.mp3"])
    pp.wait()
    pp = Popen(["avconv", "-i", "/tmp/x.wav", "/tmp/x.mp3"])
    pp.wait()
    p.stdin.write("send_audio " + title.replace(" ", "_") + " /tmp/x.mp3\n")

def img(i):
    p.stdin.write("send_photo " + title.replace(" ", "_") + " " + i + "\n")

from PIL import Image

def glitch():
    f = open("/tmp/teleglitch.jpg", 'r')

    new = f.read(400)
    for c in f.read():
        if random.random() > random.choice([0.9992, 0.9993, 0.9994, 0.9995, 0.9996, 0.9997, 0.9998, 0.9999]):
            new += chr(int(ord(c) + random.random()*random.choice(range(100)))%256)
        else:
            new += c
    fw = open("/tmp/teleglitched.jpg", 'w')
    fw.write(new)
    fw.close()
    return "/tmp/teleglitched.jpg"

answered = pickle.load(open('answered.pkl','r'))

updates = bot.get_updates().wait() #Flush first updates
for pos, update in enumerate(updates):
    answered.append(update.message.message_id)

while True:
    print ("Getting updates".center(50, '-'))
    updates = bot.get_updates().wait()
    for pos, update in enumerate(updates):
        #print str(update)
        msg = update.message.text
        if update.message.chat:
        	user = update.message.chat.id
        else:
        	user = update.message.sender.id

        if update.message.message_id in answered:
            continue

        answered.append(update.message.message_id)
        
        
        if msg.lower().startswith("qotd"):
            wrt(user, "%s" % (Popen(["fortune"], stdout=PIPE).stdout.read().replace("\n", " ")))
        elif "molej" in msg.lower():
            wrt(user, "%s" % random.choice(molejo.split("\n")))
        elif "funk" in msg.lower():
            wrt(user, "%s" % random.choice(funk.split("\n")))
        elif re.match(".*( |^)(falo|piroca)(s| |\x1b|$).*", msg.lower()):
            wrt(user, "8%sD" % ("="*random.randint(1,100)))
        #elif "xxt" in msg.lower() or "xoxota" in msg.lower():
        #    img(random.choice(glob("pussy*.jpg")))
        elif msg.lower().startswith("dia ") or msg.lower().startswith("dia!") or msg.lower().startswith("dya") or "bom dia" in msg.lower() or "bom dya" in msg.lower() or "dia!" in msg.lower():
            wrt(user, "%s" % (random.choice(bomdia.split("\n"))))
        elif "perd" in msg.lower():
            wrt(user, random.choice(perdi.split("\n")))
        #elif "[photo]" in msg and 'shirley porter' not in line.lower():
        #    p.stdin.write("load_photo %s\n" % msg_id)
        #    waiting_photo_download = True
        else:
            ss = say(msg.lower())
            if len(ss.split()) > 2:
                wrt(user, ss)
        #    if ss.strip()[:-2] in msg.lower().strip().replace(",", ""):
        #        print "SAME:", ss
        #        pass #img(random.choice(glob("*.jpg") + glob("*.png")))
        #    else:
        #        f = open("porter.txt", 'a')
        #        f.write("FALA: " + msg)
        #        f.write("RESPOSTA: " + ss + "\n\n")
        #        f.close()
        #        time.sleep(.1)
        #        if chance(5):
        #            voice(ss)
        #        else:
        #            wrt(ss
        process(msg)
        f = codecs.open("input.txt", 'a', encoding='utf-8')
        f.write(msg+'\n')
        f.close()
        pickle.dump(answered, file=open('answered.pkl','w'))