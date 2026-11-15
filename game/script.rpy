# Set a default value for the player's name

default player_name = "Aya"
define player_name_2 = "???"

# Declare characters used in the game.

define mc = Character("player_name", dynamic=True)
define y = Character("player_name_2", dynamic=True)

style button:
    hover_sound "audio/hover.ogg"
    activate_sound "audio/click.ogg"

style navigation_button:
    hover_sound "audio/hover.ogg"
    activate_sound "audio/click.ogg"

default clues = 0
default trust = 0
default music_skill = 0
default bounce_score = 0
default melody_complete = False
default knows_truth = False

transform ddlc_pop(z=1.0):
    xalign 0.5
    yalign 1.0
    zoom z
    yoffset 0
    easeout 0.1 yoffset -20
    easein 0.1 yoffset 0


# The game starts here.

label start:

    
    scene start with fade

    python:
        player_name = renpy.input("What is your name?", default="Aya").strip()
        if not player_name:
            player_name = "Aya"


# Morning wake up scene

jump act1_scene1 
label act1_scene1:

    scene black 

    play sound "audio/alarm.ogg"
    
    
    "BEEP...BEEP...BEEP"

    scene bg_bd_scene with fade

    mc "Mmmm..."
    stop sound fadeout 1.0
    "The alarm continued ringing."
    

    mc "Five more minutes...."
    "I reached towards the bedside table."

    play sound "audio/glass.ogg"
    "My hand knocked over a glass."

    


    mc "Seriously?"
    
    stop sound fadeout 1.0

    "..."
    mc "What was I doing yesterday?"

    "I tried to remember."

    "A room."

    "Bright lights."

    "A sound..."

    "Nothing."

    mc "Never mind."

    "I sighed and sat up."

    "Another ordinary morning."

    "At least, that's what I told myself."

    "I got up and decided to check my laptop."

    "No DMs..."
    "No Calls..."
    mc "Weird."

    "I decided to check my emails."

    mc "Mostly Advertisements. "
    mc "Nothing interesting."
    
    "Sigh."
    mc "I'll just wash up."

    play sound "audio/notification.ogg"

    mc "Huh?."
    mc "Who was that?"

    "{color=#FF0000}<Unknown message>{/color}"

    mc "The sender's email address was hidden."


    show screen career_message

    pause 3.0

    hide screen career_message

    mc "WHAT!"

    "I opened the email."
    "{color=#FF0000}<Hello, [player_name].>{/color}"
    "{color=#FF0000}<It's been a while since you've played.>{/color}"

    "{color=#FF0000}<Don't you miss it?>{/color}"

    "{color=#FF0000}<The applause.>{/color}"

    "{color=#FF0000}<The stage.>{/color}"

    "{color=#FF0000}<The feeling of being somewhere you belong.>{/color}"

    mc "Who the hell..."

    "{color=#FF0000}<You were once an extraordinary musician.>{/color}"

    "{color=#FF0000}<People haven't forgotten you.>{/color}"

    "{color=#FF0000}<But perhaps you've forgotten yourself.>{/color}"

    "{color=#FF0000}<If you want your career back, follow the steps.>{/color}"

    "{color=#FF0000}<STEP 1: Find the music you abandoned.>{/color}"

    "{color=#FF0000}<STEP 2: Play the melody you once knew by heart.>{/color}"

    "{color=#FF0000}<STEP 3: Return to where it all began.>{/color}"

    mc "This has to be a joke."

menu:

    "{color=#FF0000}Check the sender.{/color}":
        $ clues += 1
        "No name. No address. No trace."

    "{color=#FF0000}Delete the email.{/color}" :
        "I deleted the message."
        
"I closed my laptop."

mc "My music career..."

mc "I haven't played in years."

#THE MUSIC ROOM

scene bg_hallway with dissolve

"I walked down the hallway."

"An old door stood at the end."


scene bg_music_room with dissolve

"A grand piano stood near the window."

"I hadn’t touched it in a long time."


play sound "audio/piano_note.ogg"

"I pressed one key."

mc "A familiar sound. Have I heard it before?"

"On the piano was an old photograph."

mc "A younger version of me stood on a stage"
mc "perhaps 15, holding a trophy."

"A man stood beside me."

mc "Who is he?"

"On the back was a message."

show screen sunshine
pause 3.0
hide screen sunshine 

"Beneath it was a folded music sheet."

mc "Hmmm."
mc "Let’s see if I remember."

call melody_game

if melody_complete:
    "My fingers moved across the keys."
    "For a moment, I heard applause."
    "{color=#FF0000}<Congratulations, STEP 1 COMPLETE.>{/color}"

    "{color=#FF0000}<You did a good job.>{/color}"
else:
    "I pressed the wrong notes."
    "Why can't I remember?"
    $ reset_melody_game ()

scene bg_bd_scene with dissolve

"My laptop chimed."



"{color=#FF0000}<Tomorrow, we continue.>{/color}"

mc "Who are you?"

"The email disappeared."

scene black with fade

centered "{size=+12}CHAPTER 1: COMPLETE{/size}"

jump chapter_2
label chapter_2:


scene bg_bd_scene with fade

"The following morning. I woke up as usual. My mind went on previous day incidents. Was it even real?"

play sound "audio/notification.ogg"

"Another email."

"{color=#FF0000}<Morning Aya. Hope you are ready for today’s task.>"

mc "Why are you hiding your identity. What’s going on? Why are you making me do these tasks?"

"{color=#FF0000}<Let's prioritise execution over interrogation. Questions can wait.>{/color}"

"{color=#FF0000}<And you clearly are not in the position to choose Aya.>{/color}"

"{color=#FF0000}<Now. STEP 2: Follow the rhythm.>{/color}"

"{color=#FF0000}<Visit the old practice room.>{/color}"

"{color=#FF0000}<Find what you have forgotten.>{/color}"

mc "This is getting ridiculous."

"{color=#FF0000}<Clock is ticking Aya.>{/color}"

scene bg_practice with dissolve

"The practice room too looked familiar."

"as if i had apparently spent years here."

"Suddenly, I felt a presence behind me."

y "BOOOOOOO!!!"

mc "what the-"

"I turned to clearly see the person."
show smile at center, Transform(zoom=0.58, yalign=1.0)
y "You’re finally back."
hide smile
mc "..."

mc "Have we met?"
show upset at ddlc_pop(0.58)
y"Oh cmon now! Don’t act as if you don’t know me."

mc "Well. I don’t"  

y "You really don’t remember?"

mc "Why does everyone keep asking me that?"

hide upset
show me at ddlc_pop(0.58)

$ player_name_2 = "Yuri"
y "its me. Yuri"
hide me 
show go at ddlc_pop(0.58)
y "Anyways, the practice room is still there. You should go."
y "There's something waiting for you."
mc "Something?"
y "You'll see."
hide go

scene black with fade 
scene bg_practice with dissolve

"The room was empty."

"Two chairs stood beside a piano."

"One chair was pulled away."

mc "Was someone here?"
"I heard a faint melody."
"Then came a strange sound."


play sound "audio/distant_beep.ogg"

mc "What's that?"

"The lights flickered."
"For a second, the room looked completely different."
"White walls. Bright lights."
"Then everything returned to normal."

mc "What was that...?"
"I looked down at the music sheet."

"Notes were written on it."

#Music sheettttt  centered "{size=+10}C E G E{/size}"

mc "I know this melody."
mc "But why can't I remember where I've heard it?"
"I pressed the keys."

play sound "audio/piano_note.ogg"

"The final note echoed."

scene black with fade
"And the room disappeared."



scene bg_void with fade
"For a second, the room looked completely different."
"Darkness surrounded me."
"The same music sheet appeared before me."

mc "Again?"
mc "Why am I here?"


play sound "audio/notification.ogg"
"Your final task..."

centered "{size=+8}KEEP THE RHYTHM.{/size}"
"And no matter what..."
"DON'T STOP PLAYING."
"Don't let it fall."


call melody_game




scene bg_practice with dissolve
mc "What is happening to me?"
"My phone vibrated."

play sound "audio/notification.ogg"
"{color=#FF0000}<STEP 2 COMPLETE.>{/color}"
"{color=#FF0000}<One final step remains.>{/color}"
"{color=#FF0000}<Return to the stage.>{/color}"
mc "The stage..."
"I stared at the screen."
mc "What happened there?"
"No reply came."
"Only a blank screen."

scene black with fade

centered "{size=+12}CHAPTER 2: COMPLETE{/size}"

jump chapter_3
label chapter_3:

scene bg_bd_scene with fade

"A package came outside my door."
"i opened it and saw Inside. An old concert poster."
centered "{size=+8}AYA: THE RISING STAR{/size}"
mc "I performed here?"
"A handwritten note was attached."
centered "{i}You promised you'd finish the song.{/i}"

scene black

y "Aya."
y "Ayaaa"
y "AYAAAAAAA!!!!!!"
y"WAKE UP!!!! PLEASE!!!!!!"
scene bg_hospital with fade
mc "... "
play sound "audio/crying.ogg" 

show cry at ddlc_pop(0.58)
y "Aya..."
y "You've finally woken up."
mc "How long?"
y "A long time."
mc "I thought I'd lost everything."
y "You're here now. That's enough."
"I looked at Yuri and finally felt at peace."
mc "I'm back..."
hide cry 
scene black with fade
"A few days later."
play sound "audio/notification.ogg"
"A new email arrived."
centered "{size=+8}YOUR CAREER ISN'T OVER.{/size}"
"{color=#008000}<Hello again, Aya.>{/color}"
pause 1.5
"{color=#008000}<You woke up.>{/color}"
pause 1.5
"{color=#008000}<I'll be waiting.>{/color}"
pause 3.0


centered "{size=+30}OFFBEAT{/size}"

centered "{color=#e67ac7}{size=+30}THE END{/size}{/color}"
return


return


screen career_message():

    frame:
        xalign 0.5
        yalign 0.5

        background "#ffffff9b"
        padding (30, 20)

        text "YOUR CAREER ISN'T OVER.":
            size 40
            color "#FF0000"
            xalign 0.5

screen sunshine():

    frame:
        xalign 0.5
        yalign 0.5

        background "#00000089"
        padding (30, 20)

        text "For my sunshine. Keep playing.":
            size 34
            color "#F5B0CD"
            xalign 0.5

    




    # This ends the game.
