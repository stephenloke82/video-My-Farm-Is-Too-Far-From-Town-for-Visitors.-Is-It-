# Every spoken line of the video, in order, with the scene that carries it.
# The text here is the script, word for word. `hold` is extra silence after the
# beat, used before turning points.

BEATS = [
    # Cold open
    ("cinema", "April 1989. A baseball movie opens in cinemas.", 0.1),
    ("iowa_film", "It was filmed on a family farm, near a small town in Iowa.", 0.3),
    ("stranger_arrive", "Two weeks later, a stranger pulls into the farm driveway.", 0.1),
    ("route_map", "He is driving from New York to California.", 0.1),
    ("stranger_corn", "He went out of his way to see a cornfield, before somebody plowed it up.", 0.2),
    ("stranger_first", "He was the first.", 0.7),
    ("counter300k", "By late 1995, nearly 300,000 people had followed him.", 0.1),
    ("cars_line", "To a cornfield. In Iowa.", 0.8),
    ("yourfarm_road", "Now picture your own farm. A long road in. No highway sign.", 0.0),
    ("yourfarm_town", "The nearest town, a good drive away.", 0.1),
    ("whisper", "And a quiet voice that asks, \"Who would ever drive all the way out here?\"", 0.7),
    ("title", "Is your farm too far from town for visitors? Let's find out.", 0.4),
    ("agenda1", "In this video, we will look at how far farm visitors really travel.", 0.0),
    ("agenda2", "We will visit a real greenhouse farm, about 60 miles from the capital, that welcomed 180,000 visitors in one year.", 0.0),
    ("agenda3", "And we will walk through three moves that make a far-away farm worth the drive.", 0.1),
    ("stay3", "Stay for move number three. It decides whether a remote farm gets found, or gets forgotten.", 0.3),
    ("stephen", "This channel comes from Stephen Loke, founder of Bloopy Durians, a durian farm in Malaysia that welcomes visitors from all over the world.", 0.0),
    ("stephen4wd", "And here is the part that matters for you. Visitors reach his farm by four-wheel drive.", 0.4),

    # The belief
    ("belief", "Here is what most farmers believe. Visitors only go to farms close to town. Near the highway. Near the people.", 0.3),
    ("driveby_intro", "That belief made sense for one kind of farm. Call it the Drive-By Farm.", 0.0),
    ("driveby_stand", "A stand by the road. A hand-painted sign.", 0.0),
    ("driveby_car", "A car slows down, someone buys a bag of apples, and drives on.", 0.0),
    ("driveby_starve", "The Drive-By Farm lives on passing traffic. Far from the traffic, it starves.", 0.4),
    ("notonly", "But passing traffic is not the only way people find a farm.", 0.2),
    ("kansas", "A study of agritourism visitors in Kansas found the average visitor travelled 129 miles to get there.", 0.1),
    ("kansas_fair", "To be fair, more than half came from under 50 miles away.", 0.0),
    ("kansas_avg", "But the people who drove a long way pulled that average up, and they came on purpose.", 0.1),
    ("oregon", "In Oregon, a 2018 survey of agritourism farms found about a quarter of visits came from people who travelled 50 miles or more. One way.", 0.2),
    ("people_drive", "So people do drive. The question was never, \"How far is my farm?\"", 0.0),
    ("real_question", "The real question is, \"What's waiting at the end of the road?\"", 0.8),
    ("split1", "That is the difference between a Drive-By Farm and a Worth-the-Drive Farm.", 0.0),
    ("split2", "One waits for traffic. The other gives people a reason to plan the trip.", 0.3),
    ("notthis1", "Now, what this is not. This is not a promise that every remote farm will pull 300,000 people.", 0.0),
    ("notthis2", "And nobody is telling you to build a theme park, or to move closer to town.", 0.0),
    ("keepfarming", "You can keep farming exactly as you do.", 0.0),
    ("fix", "The fix is in what people find when they arrive, and how they find you before they leave home.", 0.5),

    # Iceland
    ("iceland_map", "Iceland, 1995. Two young graduates, Knútur and Helena, buy a run-down greenhouse farm in a small village, about 60 miles from the capital.", 0.0),
    ("fridheimar_sign", "The farm is called Fridheimar.", 0.1),
    ("grads", "He studied agriculture. She studied growing plants under glass.", 0.0),
    ("repair", "For years they repaired the place and grew tomatoes all year round, heated by water from the hot springs.", 0.0),
    ("crates", "But a tomato is a tomato. Theirs went out the gate like everyone else's.", 0.3),
    ("gate2008", "Therefore, in 2008, they opened the gate. Visitors could watch how they bred horses and grew tomatoes.", 0.0),
    ("nine_hundred", "In the first year, 900 people came.", 0.0),
    ("noticed", "Not a crowd. But they noticed something.", 0.3),
    ("warm_inside", "People loved standing inside a warm, bright greenhouse, while the Icelandic winter blew outside.", 0.0),
    ("restaurant", "So, in 2012, they put a restaurant right in the middle of the greenhouse.", 0.0),
    ("menu", "Tables between the tomato vines. Tomato soup with fresh bread. Tomato ice cream. Even tomato beer.", 0.1),
    ("picture", "Picture it. Snow outside. You sit inside, warm, eating soup made from tomatoes growing a few feet from your table.", 0.2),
    ("count180", "By 2019, they welcomed 180,000 visitors in one year.", 0.0),
    ("pct85", "About 85 percent came from outside Iceland. Today the farm employs dozens of people.", 0.0),
    ("quote", "Knútur once said tourism was supposed to be their side business. It turned into one of their main businesses.", 0.1),
    ("same", "Did they move closer to the city? No. Same farm. Same village. Same road.", 0.3),
    ("fixed", "They didn't fix the distance. They made the trip worth it.", 0.8),
    ("cta_guide", "If you are thinking, \"My farm has to be found first,\" Stephen wrote a step-by-step Google guide for farms. The link is in the description. More about it at the end.", 0.0),
    ("subscribe", "And if this is helping, subscribe, so the next farm lesson finds you.", 0.5),

    # Move one
    ("move1card", "Move number one. Give them one thing they cannot get in town.", 0.1),
    ("move1_examples", "Fridheimar had lunch inside a greenhouse. The Iowa farm had a walk around the bases of a movie ball field.", 0.0),
    ("sold_one", "Neither one sold more stuff. They sold one experience you could only have there.", 0.1),
    ("eggs", "On your farm, that might be breakfast with eggs the children collected themselves.", 0.0),
    ("fruit", "Fruit eaten straight from the tree.", 0.0),
    ("sunset", "A ride across the fields at sunset.", 0.1),
    ("test", "Here is the test. If they can get it at a supermarket ten minutes from home, it will not pull them sixty miles from home.", 0.2),
    ("sentence", "So finish this sentence. \"Only at our farm can you...\" Whatever goes in that blank is your reason for the drive.", 0.5),

    # Move two
    ("move2card", "Move number two. Make the road part of the adventure, and make the visit long enough to be worth it.", 0.1),
    ("bumpy", "Remember, visitors reach Bloopy Durians by four-wheel drive. A bumpy road that would scare off a supermarket shopper becomes the first story people tell their friends.", 0.1),
    ("hour20", "People will not drive an hour for a twenty-minute stop. But they will drive an hour for a half-day out.", 0.0),
    ("dotoeat", "Something to do. Something to eat. Something to take home.", 0.1),
    ("iceland_path", "That is exactly how the Iceland farm grew. A horse show. A walk through the greenhouse. Lunch. A little farm shop.", 0.0),
    ("earn", "Each one gives a guest another reason to stay, and another way for the farm to earn.", 0.1),
    ("tell_drive", "And tell people the drive before they ask. \"Forty-five minutes from town, and the last stretch is a farm track.\"", 0.0),
    ("expected", "A long drive that is expected feels like part of the trip. A long drive that is a surprise feels like a mistake.", 0.5),

    # Move three
    ("move3card", "Move number three. The one that decides found or forgotten.", 0.2),
    ("phone_home", "Nobody stumbles across a remote farm. Every visitor decides at home, on a phone, before the car leaves the driveway.", 0.1),
    ("three", "Google says its local results are based mainly on three things. Relevance, distance, and prominence.", 0.0),
    ("lock", "Distance, you cannot change. But the other two, you can.", 0.1),
    ("relevance", "Relevance means how well your listing matches what people search for. A complete profile, the right category, real photos, your opening hours.", 0.0),
    ("prominence", "Prominence means how well known you are. Google says reviews and links from other websites play a part.", 0.1),
    ("nopay", "And here is the good news for a farm without a big budget. Google says there is no way to pay for a better local ranking.", 0.2),
    ("found_forgot", "The Drive-By Farm is found by accident. The Worth-the-Drive Farm is found on purpose. That is the difference between a remote farm that gets found and one that gets forgotten.", 0.5),

    # The objection
    ("hours", "Maybe you are thinking, \"My farm is not 60 miles out. It is hours out.\"", 0.2),
    ("honest", "Here is the honest answer. The further away you are, the bigger your reason has to be.", 0.1),
    ("halfday", "An hour out, a half-day experience works.", 0.0),
    ("cabin", "Several hours out, people need somewhere to sleep. Tents. A cabin. A farm stay. Then the distance stops being a drive and becomes a getaway.", 0.1),
    ("bar_gate", "Distance raises the bar. It does not close the gate.", 0.7),

    # Close
    ("back1989", "Think back to that stranger in 1989. He didn't care how far the farm was. He cared about what was waiting there.", 0.4),
    ("doing", "Watching this won't change anything. Doing will.", 0.3),
    ("homework", "So here is your homework. In the comments, finish the sentence, \"Only at our farm can you...\" and tell us how far you are from the nearest town.", 0.2),
    ("guide", "Then, if you want to be found before people leave home, get Stephen's Google guide for farms. It's called \"Stop Being the Best-Kept Secret in Your County.\"", 0.1),
    ("inside", "Inside, you will see the three farms Google shows first and what wins those spots, a farm category guide, a fifteen-shot photo list, scripts for asking for reviews, reply templates, and a thirty-day plan with a fifteen-minute weekly routine.", 0.1),
    ("guarantee", "It comes with a thirty-day money-back guarantee. Click the link in the description, and the guide downloads straight away.", 0.2),
    ("next", "Next, watch \"Start Agritourism With What You Already Own.\" It shows how to open the gate without a loan.", 0.4),
    ("final", "Don't fix the distance. Make it worth the drive.", 1.0),
]

END_SCREEN_SECONDS = 20.0

# Written for the voice only. Captions keep the script's own digits.
SPOKEN = [
    ("1989", "nineteen eighty-nine"),
    ("1995", "nineteen ninety-five"),
    ("2008", "two thousand eight"),
    ("2012", "twenty twelve"),
    ("2018", "twenty eighteen"),
    ("2019", "twenty nineteen"),
    ("300,000", "three hundred thousand"),
    ("180,000", "one hundred eighty thousand"),
    ("129", "one hundred twenty-nine"),
    ("900", "nine hundred"),
    ("85", "eighty-five"),
    ("60", "sixty"),
    ("50", "fifty"),
]

# Hand phonemes, misaki notation, for names outside its dictionaries.
PHONEMES = {
    "Knútur": "knˈutəɹ",
    "Fridheimar": "fɹˈɪðhAmɑɹ",
    "Loke": "lˈOk",
    "Bloopy": "blˈupi",
    "agritourism": "ˈæɡɹətˌʊɹɪzəm",
    "Agritourism": "ˈæɡɹətˌʊɹɪzəm",
}
