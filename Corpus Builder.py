import mido
import csv
import os
import sys

FileName = sys.argv[1]
os.chdir(os.path.join('../',FileName)) #assigns working directory

mid_files = [file for file in os.listdir(os.path.join(os.getcwd(),'MIDI Files')) if file.endswith('.mid')]  #summons all the midi files in the directory

if os.path.isfile('Corpus.csv'): #creates a new csv file every time the code is run
    os.remove ('Corpus.csv')


NoteLookup = { #Maps note values (modded by 12) to pitches
    0 : 'C',
    1 : 'C#/Db',
    2 : 'D',
    3 : 'D#/Eb',
    4 : 'E',
    5 : 'F',
    6 : 'F#/Gb',
    7 : 'G',
    8 : 'G#/Ab',
    9 : 'A',
    10 : 'A#/Bb',
    11 : 'B'
}

DenomTranslate = { #Maps time signature denominators to assigned note values (denominator of "8" sends to "eighth note" value of 2)
    1 : 16,
    2 : 8,
    4 : 4,
    8 : 2,
    16 : 1
}

KeySigTranslate = { #Maps key signature to modular values
    'C' : 0,
    'Db' : 1,
    'C#' : 1,
    'D' : 2,
    'D#' : 3,
    'Eb' : 3,
    'E' : 4,
    'F' : 5,
    'F#' : 6,
    'Gb' : 6,
    'G' : 7,
    'G#' : 8,
    'Ab' : 8,
    'A' : 9,
    'Bb' : 10,
    'A#' : 10,
    'B' : 11,
    'Cm' : 0,
    'Dbm' : 1,
    'C#m' : 1,
    'Dm' : 2,
    'D#m' : 3,
    'Ebm' : 3,
    'Em' : 4,
    'Fm' : 5,
    'F#m' : 6,
    'Gbm' : 6,
    'Gm' : 7,
    'G#m' : 8,
    'Abm' : 8,
    'Am' : 9,
    'Bbm' : 10,
    'A#m' : 10,
    'Bm' : 11,
}

ScaleDegreeTranslate = { #translates chromatic scale degree into diatonic scale degree
    0 : '1',
    1 : 'b2',
    2 : '2',
    3 : 'b3',
    4 : '3',
    5 : '4',
    6 : 'b5',
    7 : '5',
    8 : 'b6',
    9 : '6',
    10 : 'b7',
    11 : '7',
}

if not os.path.isfile('Lyrics.txt'): #creates Lyrics.txt file if it's not there
    with open('Lyrics.txt', 'w') as fp:
        pass

LyricDict = {}
LyricFile = open ('Lyrics.txt', 'r+', encoding='utf-8') #references Lyrics.txt
for line in LyricFile : 
    line = line.split('-') #seperates title from rest of the lyrics
    Lyrics = line[1].strip().split(' ') #seperates each lyric from each other
    LyricDict[line[0]] = Lyrics #sets Lyrics array as a Dict

with open ('Corpus.csv', 'w', newline='', encoding='utf-8') as f: #Lets us write in a csv file
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerow(['SongName','TrackName','TimeSig','KeySig','Measure Number','NoteValue','ScaleDegree','NoteLyric','NoteLength','SecondNoteLength','MetricPlacement','Tempo'])


for track in mid_files: #iterates through each track in each midi file
    mid = mido.MidiFile(f'MIDI Files/{track}')
    
    SongName = track[:-4] #sets the name of the tune, :-4 removes the ".mid" from file name
    
    LyricLine = LyricDict[SongName] if LyricDict and SongName in LyricDict else [] #fetches a list of NON-ENGLISH lyrics that come from the Lyrics.txt file
    
    MiliTempo = mid.tracks[0][2].tempo
    Tempo = 60000000 // MiliTempo #Calculates tempo (Mido gives tempo in miliseconds)

    TimSigDenom=DenomTranslate[mid.tracks[0][0].denominator]
    MetricMod = mid.tracks[0][0].numerator * TimSigDenom #Calculates the variable by which we mod in order to find the metric placement of each note
    TimeSig = f'{mid.tracks[0][0].numerator}/{mid.tracks[0][0].denominator}' #sets the time signature to a string format
    KeySig = mid.tracks[0][1].key #finds key signature
    KeySigMod = KeySigTranslate[KeySig]
    

    with open ('Corpus.csv', 'a', newline='', encoding='utf-8') as myfile: #Lets us write in a csv file
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for track in mid.tracks[1:]: #iterates through each message in each track
            Measure = 1 #initializes Measure number
            MetricPlacement = 0 #initializes metric placement variable at the downbeat
            LyricI = 0 #initialize variable to index each lyric in a song; resets to 0 for each tune
            L = None #initializes lyric variable
            for msg in track: #iterates through all the messages in current track
                # print(msg) #prints messages to see what's up
                if msg.type == 'track_name':
                    TrackName = msg.name #fetches track name
                    pass
                if msg.type == 'lyrics' :
                    L = msg.text #assigns English lyric to variable L
                    pass
                if msg.type == 'note_off' :
                    NoteValue=NoteLookup[msg.note % 12] #assigns variable to note pitch
                    ChromScaleDegree = (msg.note - KeySigMod) % 12 #assigns chromatic scale degree to note
                    ScaleDegree = ScaleDegreeTranslate[ChromScaleDegree] #turns chromatic scale degree into diatonic scale degree
                    NoteLength=msg.time / 240 #calculates the metric length of note
                    if NoteLength.is_integer() : #checks if NoteLength is a triplet
                        NoteLength = int(NoteLength)
                    else :
                        NoteLength = round(NoteLength,2)
                    SecondNoteLength = (NoteLength/4)*(60/Tempo) #calculates the length, in seconds, of the note
                    SecondNoteLength = "{:.3f}".format(SecondNoteLength) #truncates decimals
                    if float(MetricPlacement).is_integer() : #checks if MetricPlacement is an integer and then rounds it
                        MetricPlacement = int(MetricPlacement)
                    NoteLyric = LyricLine[LyricI] if LyricLine else L #if non-english -> refers to Lyrics.txt | if english -> refers to MetaMessage
                    wr.writerow([SongName,TrackName,TimeSig,KeySig,Measure,NoteValue,ScaleDegree,NoteLyric,NoteLength,SecondNoteLength,MetricPlacement,Tempo]) #writes all the information into .csv file
                    if (MetricPlacement + NoteLength) >= MetricMod :
                        Measure = Measure + ((MetricPlacement + NoteLength) // MetricMod)
                        Measure = int(Measure)
                    MetricPlacement = (MetricPlacement + NoteLength) % MetricMod #adjusts metric placement for next note
                    LyricI = LyricI + 1 #increase variable by 1 to get to next lyric
                elif msg.type != 'note_off' :
                    # print(msg)
                    RestLength=msg.time / 240 #calculates the metric length of rest
                    if RestLength.is_integer() : #checks if RestLength is a triplet
                        RestLength = int(RestLength)
                    else :
                        RestLength = round(RestLength,2)
                    if (MetricPlacement + RestLength) >= MetricMod :
                        Measure = Measure + ((MetricPlacement + RestLength) // MetricMod)
                        Measure = int(Measure)          
                    MetricPlacement = (MetricPlacement + RestLength) % MetricMod #adjusts metric placement for next note
                
          
LyricFile.close()
