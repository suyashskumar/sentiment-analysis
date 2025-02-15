import pandas as pd
import random
 
# Expanded and diverse comments for realism
normal_comments = {
    0: [
        "I regret buying this. The quality is terrible, and it stopped working within a week.",
        "Absolutely disappointing. It doesn’t match the description at all. Waste of money.",
        "This was a huge letdown. I expected something decent, but it barely functions.",
        "The material feels cheap, and it started breaking apart in just a few days.",
        "I tried contacting support, but they didn’t even bother responding. Terrible experience."
    ],
    1: [
        "It’s okay, but not great. I expected better quality for the price.",
        "Works, but not efficiently. You’ll need patience to deal with its flaws.",
        "Not a complete disaster, but far from impressive. Feels cheaply made.",
        "Expected more, but it’s functional at least. Won’t recommend but won’t completely dismiss it either.",
        "It’s fine, just not worth the hype. There are better alternatives available."
    ],
    2: [
        "Does the job, nothing more. Average product, not too bad but not amazing either.",
        "It’s usable, but don’t expect anything extraordinary. It’s just okay.",
        "It works, but I wouldn’t say I love it. It’s decent but forgettable.",
        "Not bad, but not something I’d go out of my way to recommend.",
        "It’s fine for the price. Nothing exceptional, but no major complaints either."
    ],
    3: [
        "Surprisingly good! I didn’t have high expectations, but it works well.",
        "Reliable and functional. Happy with my purchase overall.",
        "A great balance between price and performance. Worth considering.",
        "Solid product! Not perfect, but definitely a good purchase.",
        "Pleasantly surprised by the quality. Would recommend to others."
    ],
    4: [
        "Absolutely amazing! Exceeded all my expectations. Perfect in every way!",
        "This is exactly what I needed! Works flawlessly and worth every penny.",
        "Best purchase I’ve made in a long time! Highly recommended!",
        "The quality is top-notch, and it works better than advertised. So happy with it!",
        "If you’re considering buying this, go for it! You won’t regret it!"
    ]
}
 
sarcastic_comments = {
    0: [
        "Wow, just what I needed—a product that breaks after one use. Fantastic!",
        "This is truly a masterpiece… of terrible design. Love wasting my money!",
        "Oh, it’s great! If your idea of fun is constantly troubleshooting a broken product.",
        "I must say, this product has redefined disappointment for me. Bravo!",
        "Absolutely phenomenal—if you enjoy spending money on things that don’t work."
    ],
    1: [
        "It’s functional… barely. If you enjoy surprises, this is for you.",
        "Oh, it does work! Just not in the way it’s supposed to. A truly magical experience.",
        "It exists. And that’s about the best thing I can say about it.",
        "It functions… just enough to keep you from throwing it away immediately.",
        "Well, at least it turns on. That’s something, right?"
    ],
    2: [
        "Oh, it’s definitely a product. Does it work? That’s up for debate.",
        "I had zero expectations, and somehow, I’m still disappointed. Impressive!",
        "It’s functional but makes you question your life choices every time you use it.",
        "Not terrible, not great. Just floating in a sea of mediocrity.",
        "It gets the job done… in the slowest and most frustrating way possible."
    ],
    3: [
        "I’m actually surprised—this almost works properly! Almost.",
        "For once, I got something that didn’t completely disappoint me. Refreshing!",
        "I expected disaster, but it’s actually decent. Maybe the universe is feeling generous today.",
        "It’s not perfect, but at least I don’t regret my purchase. Progress!",
        "Would I recommend it? Maybe. If you enjoy unpredictability in your life."
    ],
    4: [
        "Wow, this is just perfect! I might cry tears of joy. If only everything in life worked this well!",
        "This exceeded all my wildest dreams! I never thought I’d see such perfection.",
        "I am truly speechless. This is so flawless it must have been crafted by divine beings.",
        "If all products were like this, we’d be living in a utopia. Absolute perfection!",
        "This is the best thing since sliced bread. No, actually, it’s even better!"
    ]
}
 
hindi_comments = {
    0: [
        "Bekar hai, paisa barbaad ho gaya. Ek hafte me kharab ho gaya.",
        "Bilkul bekaar. Jo likha hai, uska aadha bhi sahi nahi hai.",
        "Ye toh sabse bekar cheez hai jo maine kabhi kharidi hai.",
        "Puri tarah se disappointing. Bilkul bhi kaam ka nahi hai.",
        "Itni buri quality expect nahi ki thi. Yeh toh ek dum ghatiya hai."
    ],
    1: [
        "Kaam toh karta hai, par behtar ho sakta tha.",
        "Thoda disappointment toh hai, lekin itna bura bhi nahi hai.",
        "Ek average experience raha, kuch khaas nahi.",
        "Ek normal product hai, zyada umeed mat rakho.",
        "Zyada accha nahi, lekin chalta hai. Paisa pura vasool nahi hua."
    ],
    2: [
        "Kaam chalane layak hai. Na achha na bura.",
        "Bohot zyada tareef nahi kar sakta, lekin bekar bhi nahi hai.",
        "Agar aur koi option nahi mile toh theek hai.",
        "Itna bhi bura nahi hai jitna socha tha.",
        "Na bekar na accha, beech ka hai."
    ],
    3: [
        "Mujhe laga tha bas theek thaak hoga, lekin yeh kaafi accha nikla!",
        "Koi dikkat nahi aayi, sab kuch smooth chal raha hai.",
        "Is price range me kaafi accha option hai.",
        "Agar ek reliable product dhoond rahe ho toh yeh sahi hai.",
        "Samay par delivery mili aur product bhi sahi kaam kar raha hai."
    ],
    4: [
        "Bilkul perfect! Aise lag raha hai jaise specially mere liye banaya ho.",
        "Bina soche samjhe le lo, yeh best hai!",
        "Mujhe nahi laga tha ki yeh itna badhiya niklega.",
        "Agar har cheez aisi hoti toh duniya kitni acchi jagah hoti!",
        "Ekdum zabardast! Aaj tak ka best purchase!"
    ]
}
 
# Generating data
data = []
for i in range(1000):
    for category in [normal_comments, sarcastic_comments, hindi_comments]:
        sentiment = i % 5  # Ensuring even distribution of sentiments 0-4
        comment = random.choice(category[sentiment])
        data.append([sentiment, comment])
 
# Creating DataFrame and saving to CSV
df = pd.DataFrame(data, columns=["Sentiment", "Comment"])
df.to_csv("sentiment_comments.csv", index=False, encoding="utf-8")
 
print("CSV file 'sentiment_comments.csv' has been generated successfully!")