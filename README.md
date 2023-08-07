This code compiles information from MIDI files with single-note melodies and creates a corpus (in the form of a .csv file) with a lot of information about the collection of music. The .csv will include obvious things such as each song name, time signature, tempo, and key signature, but will also include very specific details regarding each individual note, such as pitch, the measure and beat in which the note was played, the scale degree (in relation to the key signature), and the amount of time (in both beats and seconds) that the note is held. The .csv will also include the lyric attached to each note, and, with a little extra work, is capable of interpreting different languages.

# How to run
Create a new folder as a parent directory for all the files related to this project. Within that parent directory, create a folder called 'MIDI Files' and place all MIDI files there.

In Python 3.0+, create a python virtual environment using  
`python3 -m vmv <environment name>`  
`source <environment name>/bin/activate`  
`pip install -r requirements.text`

After making the virtual environment, run  
`python 'Corpus Builder.py' <parent directory>`

Afterwards, all the data should be visible in a file called 'Corpus.csv'.

# How to run with non-English lyrics
MIDI files have a hard time understanding non-English languages. In the creation of this project, we were working with MIDI files with Korean lyrics and created a solution that comes with a bit of extra manual work.  
Create a text file called 'Lyrics.txt'. Each line will include the name of one MIDI file, alongside the lyrics of that file in the following format:

```
<MIDI file name>- Lyric1 Lyric2 Lyric3 ...
주 살아 계시고- 주 살 아 게 시 고 날 사 랑 한 다 는 이 진 리 내 게 성 령 이 말 하 여 주 누 나 말 하 여 주 누 나 
감사합니다- 하 나 님 아 버 지 감 사 합 니 다 사 랑 자 비 친 절 베 풀 어 주 시 고 부 모 와 친 구 들 또 집
송아지- 송 아 아 지 송 아 아 지 업 룩 송 아 지 엄 마 소 도 업 룩 소 엄 마 마 닮 았 네
Amazing Grace- A ma zing zing grace how sweet the sound that saved a a wretch like me I once was was was lost but now am am am found Was blind but but now I see
```

At a glance, the 'Amazing Grace' example looks stupid because of the consecutive repeated lyrics, but this is an unfortunate necessity for this project to work. If there is a single syllable that is held out over multiple consecutive notes, it is necessary to type **the full syllable for each of those notes**. See the above lines as an example, as well as our own ExampleLyrics.txt file.  
Once the Lyrics.txt file is complete and contains all the lyrics of all your MIDI files, you can run the program using the same lines of code as before.  
`python 'Corpus Builder.py' <parent directory>`

# Limitations
1. The manual work required for non-English lyrics proves to be quite arduous when dealing with very many MIDI files. While it's easy to copy and paste lyrics from any modern music notation software, it is cumbersome to have to manually type in the necessary repeated lyrics for each MIDI file.
2. This project only works with **single-note melodies**. Currently, the code does not have the ability to process two notes occuring contemporaneously, thus MIDI files must only contain single-note melodies. Multiple tracks, however, are fine. Since this project was initially designed to study the melodic tendancies of Korean folk music, this was never a problem for us, but is something that could be improved upon in the future.
3. .csv is a complicated file type, and can include more than one specific type of .csv. Because of this, Microsoft Excel doesn't have an easy time understanding non-English details that are exported into the .csv file. The workaround we used for this was to simply open the .csv file in Google Sheets, which worked well every time.
