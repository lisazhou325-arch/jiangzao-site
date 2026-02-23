# How to Make Claude Code Better Every Time You Use It (50 Min Tutorial) | Kieran Klaassen

**Platform:** YouTube
**URL:** https://www.youtube.com/watch?v=g6z_4TMDiaE
**Source:** Peter Yang

---

完整字幕

00:00 AI can learn, which is really cool. So, if you invest time to have the AI learn what you like and learn what it does wrong, it won't do it the next time. The beauty is that all these things together are synthesized into kind of a story to me. Making sure those learnings are captured and then the next time you create a plan, it's there. It learns. So, that isn't a compound play, right? It's like a QA team. Basically, you don't even need to write the test. You just say, "Yo, just test it." So if something breaks, it can fix it immediately and immediately validate whether it fixed it. The LFG command. So I have this command now. Everything we just did, testing and creating a video and creating a pull request and it just runs for an hour and it does it.

00:49 Hey everyone, I'm really excited to welcome back Kieran today. Karen is a CTO for Kora at every and also my favorite clock code power user. So Kieran is going to show us how to do compound engineering so that cloud code gets better each time you use it and he'll also show us his exact clock code setup to manage multiple agents and a lot more. I'm basically going to pick his brain a lot in this episode. So welcome Karen.

01:14 >> Thank you so much. I know last time uh I really enjoyed talking to you and I'm very excited to show and share with everyone what I learned uh because close code is picking up. Lots of people are using it now.

01:27 >> Yeah. It feels like half the conversation on social media is about clock these days. So yeah.

01:31 >> Yeah. We're like we're in a bubble but like I think the bubble is expanding a little bit which I love because more people can create which is amazing.

01:40 >> All right. So I'm going to share this slide. Okay. Okay. So I I made this janky slide on compound engineering based on what you wrote and uh do you want do you want to just cover this thing at the high level and then we can get into like the actual clock code?

01:54 Yeah. Yeah. Absolutely. So compound engineering is uh it's a philosophy really that I invented when I was building Kora and it's just best practices that I just learned from using AI and especially this started with uh cloth code when cloth code launched a year ago um cuz there were things that worked and didn't work and they were frustrating so I built a philosophy and what I really figured out very quickly was like AI can learn uh which is be cool. So if you invest time to have the AI learn what you like and learn what it does wrong, it won't do it the next time. So that's the seed for compound engineering. Um yeah, and there are four steps in the compound engineering philosophy, uh which is planning first, um working, which is just doing the work from the plan. Then it's assessing and reviewing, making sure the work that's done is correct. and then taking the learnings from that process uh and codify it. So this is the compound aspect. So the point is for example if you make a plan do the work and then assess whether it's good. It's never completely exactly the right thing. There's always feedback or things that weren't exactly or you learn something. So making sure those learnings are captured and then the next time you create a plan it's there. It learned. So that's really the the philosophy of the loop and I have a plugin as well for that and we'll go into that. So it's a philosophy. It's also a plugin that I built that you can use and yeah that's the high level of uh of everything.

03:34 >> Awesome.

03:35 >> Let me show you what a flow like this looks like. So the four steps. So first if you want to follow along you can do that yourself as well.

03:44 >> Mhm.

03:44 >> I have my terminal open here. It's warp. I have cl code running in bypass permissions. So, skip dangerously. That's how I like to go. [laughter] If you Yeah, we'll we'll we can go into like when to use what. Uh that's how I run it. I'm just pushing things to go as fast as possible. If you want to follow along, this is the repo. So, you run these commands. Uh the compound engineering plugin, you need to add it and then install it. And then you have the exact same flow as I have. So, you can just do this in your own project and follow along. So the first thing is what are we building and I am on this quest of making Kora agent native and yeah Kora is my product. It's a email assistant that screens your inbox and briefs twice a day and there's a assistant as well inside the product and the idea of agent native is that the assistant or the agent within the app can do exactly the same thing as the user can do. So like if you can go to settings for example in your app then if you talk to the agent and say can you change these settings the agent should be able to do exactly the same. So I'm trying to get to par there because uh like it's a very important thing because it enables agents to come up with new ways of working and it's really inspired by how cloth code works like cloth code has access to your computer and can just do anything on your computer and we figure out all these cool flows and things we can do suddenly with cloth and it's similar you can bring that same spirit to your app. So what we're going to do is we're going to plan and uh it's called workflows plan since plan is now taken by the internal systems of cl code. So workflows plan and you give a description of what you want to do and I will use a monologue which is voicetoext app. Uh I don't like typing too much so we'll we'll we'll do that. Um and I'm going to explain what I want. I want to create um feature parity with all of the things we can do in settings. So any settings the user can do in any of the views. I want to make sure that the Kora assistant can change the same things as the user. So make sure we look first for everything we can do as a user and then make sure to uh see how the assistant can do that. So through tools through whatever we want and you can look at the agent native skill to uh learn how to best do this. So I give some direction here and it's going kick off here now and we can kind of uh see what it is going to do and why it's doing those things. So any questions so far or this episode is brought to you by Granola. If you're in backtoback meetings, you know how much work it is to take notes live and clean them up afterwards. That's why I love Granola, the best AI meeting notes app in the market. Here's how I use it. Granola automatically takes notes during a meeting. And I can add my own notes, too. After the meeting ends, I use a Granola recipe to extract clear takeaways and next steps in the exact format that I want. Then I can just share notes directly in Slack with my colleagues or even get Granola to share notes automatically. Honestly, of all the AI apps that I use, Granola is the one that saves me the most time. Try it now at granola.ai/ AI/peter and use the code Peter to sign up and get three months free. That's granola.ai/peter.

07:28 Now back to our episode. I'm really curious what's doing behind the scenes like is it making a snip or looking through the code?

07:34 >> Yeah.

07:34 >> Yeah. So so this is like you hear this in different places like you specdriven development, you have like taskmaster like like all these things you have planning mode and this is basically the planning mode from cloth but it it's a little bit beefier. it's a little bit more uh it will use more tokens but also it will do better research and really the points here is um it looks at your current code so it grounds itself in what you already did. So if there are patterns it will pick up those patterns. It will look online it will go search for articles that have been written about this and like what are the best practices. So this is what others say is good which is also very uh very handy and it goes look through frameworks you use. So if you use specific frameworks or libraries it will go look up like also it will check what version you use. So it's also important to yeah use the correct versions because otherwise there might be a mismatch. So just making sure everything is correct. So those are the first three agents here and these agents run as sub agents which means the context will be separate from the main thread. And you can see it's already like 56,000 tokens, 77,000 tokens, [snorts] 35. So it's like it's it's not cheap on the tokens, but that's not the point. The point is

08:56 >> on the max plan. Yeah.

08:58 >> Yeah. You have to be on the max plan to because otherwise you run a few and you're out. Uh but also the max plan is not very expensive. If this is your job, if you make money doing code, yeah, this is clearly uh value for the money and also you if you want to experience what the future is going to be and really push yourself like, hey, how is it going to be?

09:18 >> Um yeah, you should just push yourself because uh yeah, like our our CEO Dan at every he always pushes me a little bit because I'm like, "Yeah, but we need to look at the cost for this and it will cost us like hundreds of thousands of dollars if we just switch to the new model." and he says

09:35 >> yeah but we should also know what we can do now and if we don't know we just get stuck in the past so this is also for you as a developer if you feel like I'm very scared I want to see what's happening here I want to feel what's going on I want to see the code um let it go a little bit and just experiment with like how does it feel if you don't see what's happening here because it is a complete mind shift as well

10:03 >> I mean like Well, like how much does the average developer cost per hour? Like you know the the $200 $100 will pay for itself.

10:09 >> It's nothing. It's nothing. Yes.

10:11 >> Yeah.

10:12 >> Yeah. So

10:13 >> exactly. Yeah. So like the goal uh so the goal of this like is to get a really good plan and then we as humans look at the plan. Uh but obviously the goal long term is you just say one thing and it's done. So this is just getting getting towards a place where we know and trust certain steps and flows.

10:38 >> Yeah.

10:38 >> Uh to get us to a goal. So yeah. So at the end I'll I'll share one other command I have that just does everything in one go. So you don't need to even understand what all the steps are. Uh because I think that's going to be interesting and very helpful soon as well. But if you are a developer, you want to know what's going on here because you want to tweak this. You want to make your own. You can use my plugin obviously, but like

11:04 >> even better is to use my plugin, see what works, what doesn't work, and make your own version of that or make your own flow so you really understand what's happening. And once you do, you can just let it go. Yeah.

11:17 >> Yeah. I love the I love the best practices researcher and framework researcher because I I think if you just use plan mode in clock code it's not it's going to look at your codebase but it's probably not going to do this other stuff right

11:28 >> yeah it's like it's good for for like small things I I use plan mode and obus 4.5 is pretty good

11:35 >> in doing things but this is just it's it's a little bit better but I hope like at some point uh Boris will just copy paste this into uh into cloth code and we'll have everything working well. So like like my goal is not to have a system like ideally I delete this entire flow and everything works already. But

11:56 >> I mean Boris is basically copying man like he already copied your compound engineering so [laughter]

12:00 >> and he's inspired.

12:03 >> He is inspired. Yes.

12:04 >> He's not been paying attention. So

12:06 >> yes. Yeah. Yeah. Yeah. I I know he's inspired but also like I like um Yeah. But but he's do like he's letting people figure out what they should build and then they're like building it and and that's is really really nice.

12:22 >> The funny thing about Boris is like he went on vacation for for like for like a week and then he shipped like 50 PRs or something right on Twitter. [laughter] So I'm I'm just wondering if he's actually working like how how much does he ship shipping? Like how do you keep track of that?

12:35 >> At least 100% is AI written by him now. So and and I agree uh like I think for me it's also 100% now and yeah I haven't opened cursor other than looking at text files in like the last 3 months I think. Yeah.

12:50 >> Okay. And while we wait like what what what terminal is what what terminal app is this?

12:55 >> Yeah I use warp. I like warp since

12:58 >> yeah warp and it's AI based uh terminal as well. um which is handy if you like do things like with git and it doesn't work you say just fix this and then it will also fix it. So I I like warp also I like that you can like split paints easily. Um

13:15 >> yeah it

13:16 >> it's it's the one I like best. So okay so let's see um he did this uh is looking at the agent native architecture skill. So this is something I said to look at here. I said hey can you check the agent native skill

13:33 >> because we have this like what we try to do if there are specific information that's important we try to distill it in skills and that means you can put a lot of information in one place uh so for example this one uh here let's open it here agent native architecture so this is a very extensive long document about how to build apps like this. And there are lots of references here as well. And if you load all of this in context, you would just kill your context. But it's too much.

14:13 >> It's too much. But it's also very good to have access to this. So a skill is this way uh like it's kind of just in time context. So whenever you need it, it will like think like, oh, do I need it now? it will pull in that skill file and then if it needs even more it can look at the the resources inside there or you can run scripts. So this is way to put things like around a specific subject or a tool or a skill that it can use then. So I love that and you can like create your own skills that you reference and this is a way to make the compound engineering plug-in yours where you have your skills. For example, if you do iOS development or you have like a like a Go CLI thing going on, like I don't have any of that in in my plug-in, but you could have your skills and the compound engineering plugin will read your skills as well and we'll also apply these. So, this is a way to make it your own. Uh, and yeah, I can advise that for sure.

15:16 >> And and and you're basically uh you're obviously not handwriting the skills, right? like you're basically getting no no skills. No. Yeah.

15:22 >> So there is a there is a skill uh create agent skill uh in the combat engineering plugin as well. I think there are others but that's the one I have. I think there are some from anthropics themselves as well. So yeah don't write handwritten skills. No but make sure to read them and review them and see if it makes sense and is if it's good. Okay. So it did that uh is now doing the spec flow analyzer. So I introduced this as I noticed that sometimes it zooms in on things a lot and it show yeah it it it like figures out I need this plugin and this page and it's so zoomed in that it forgets that it's part of a bigger picture and sometimes it just forgets a complete page or thing or it does it's not hooked up to a flow or something like that. So the specflow analyzer is like imagine you're a user with like specific uh personas and go through do you miss anything? Do did we miss anything in the planning and that's very uh yeah very good to have uh like this. So that's the last step and then it writes the plan and then you can do other things. So let's let's see what it does here what the plan is. Okay so it is done with uh the writing of the plan which is great. Um, and it will ask me what to do next. So, there are a few things we can do here. Can open the plan in editor, which means let's look at it. I like to use an editor or like a viewer because I like to feel really good about the design of whatever I'm reading.

16:58 >> So, we're going to do that. But there's another option, deepen plan, which is like it just goes ham. It loads everything. It can load and reviews the plan, does any like any skill you have every like it just goes wild. And this is just like if you v code, this is great. You can also trigger this uh like automatically uh from the start, but it just goes ham on tokens and does everything it wants. Uh and it's cool when you v code because like there's nothing to lose really and you have tokens left. So yeah, why not?

17:29 >> Yeah, why not? Yeah.

17:30 >> So uh the next one is the plan review. If you want to review the plan not manually but you want like an agent to look at it this is handy. So if if you don't want to read it or you can say yolo start work um let's normally I open plans and this is also good you can share it with your team with other people. You can ask for feedback like RFC however you want.

17:54 >> Mhm.

17:54 >> I use a an app uh to read my markdowns and I like it like this because it looks pretty

18:01 >> instead of the terminal. It's It's just more pleasant to look at very boring plans and specs and things. If it looks nicer, I'm just more like it's just nicer. So, I I have this app and I uh

18:15 >> You vod?

18:16 >> No, this is a typora, but I I already had people reach out that said they vioded a free version. This is 10 bucks or so, so it's not a lot, but okay.

18:25 >> The theme is widy. So, if people want to

18:30 >> All right. Okay. witty witty or something. Uh so assistant feature parity enable core assist to modify all uh settings. So

18:40 analysis it says hey uh okay so general um so addit user doesn't exist. Um categories reordering doesn't exist but most of it brief settings is there subscriptions is not there and tokens also. So actually we're pretty good. We just need the general the user addit we need.

19:06 >> Mhm.

19:06 >> Um and okay so blah blah blah blah security. So like these come from different places. There are different angles to a plan always. So briefs is one. It does like I like to have an example piece of code like pseudo codes because I can already feel or see if this is completely wrong if I see any red flags or not. But uh

19:31 >> it it looks it looks pretty good. So So up time zone. Okay. So it has different different tools. So I my question is now um so my like I'm an engineer. So if you're not an engineer, you could say yeah I have no idea what this is and just do it. Which is perfectly fine. I think this is this is a good good thing to do. But if you are an engineer and have opinions, this is a point where you can compound or iterate. So let's try that. So because like I yeah I see all these tools but I also think these are a lot of tools. Can we not somehow consolidate this? So so let's see. Okay, I see you create and add a lot of individual tools. Is there a way where we can create one tool that can do multiple settings so it's less heavy? What about that? What do you think about that? Yeah. So, let's see what it does. So like

20:32 >> and it's it's important to do this here because if you already started implementing this and you're like an hour further, it's it's or half an hour further or more tokens further. like it's more hard it's harder to take take a step back and say no or rewrite or like you have all these things. So like if you do it if you spend time uh it's better here. So

20:54 >> okay so benefits uh yeah sure we can do update settings tool um and what I want to do is I want to compound this knowledge because I think this is like this is better. So I want to say compound boom. So I'm going to run the compound flow and it will understand from the context here what it is about

21:14 >> and it will start to create some documentation about uh things like this. So next time when it starts uh writing a plan it will pull in that information and ideally never make this mistake anymore

21:29 >> like like where is it going to write the instructions though like just the default?

21:33 >> Yeah.

21:34 >> Yeah. So there there's a a docs directory um and it will organize learnings inside the docs directory and cloth in planning will then look for things that thinks might be relevant. So there's some front matter in the top so you can search on keywords as well. But it also has uh it also has the uh option to update your cloth MD file. Like a very easy way of to do compound engineering is just saying can you update my my cloth MD file. So if you don't have the plugin and you want to compound it's just like hey don't make this mistake again add this to cloth MD. This is like the the easiest way to do it. But uh

22:16 >> yeah,

22:17 >> that that that's basically the prompt, right? You just update because that that thing gets inserted into the prompt each time.

22:23 >> Yeah, exactly. So anything that is in your cloth MD file will always be inside the prompt. So it will follow pretty directly. So if you want to start with a very light version of this, if you see it make a mistake, just say hey add this to cloth MD. And I do this all the time actually as well because sometimes it is something like a general knowledge not very specific. It's like hey how do you start the server for example or like it tries to do something in a weird way and like it should just never do it and then I'll say just store it to clothd I don't use the compound flow. So so yeah it's not one or the other. You can use everything together. It's cloth code and it all works together. So

23:03 >> got

23:03 >> yeah you can see here it's storing it in architecture decisions

23:08 uh in solutions and docs uh which is available then as well and it looped through other things I already have. So if it's related it will uh append it there and it will consolidate it. So and the beauty is this is just files in your repo and cloth reads files in your repo and is really good at that. So yeah, uh yeah,

23:30 >> I interviewed someone else who Yeah. who she has like extensive documentation for Claude and

23:35 >> uh she doesn't sometimes doesn't even read what whatever Cloud updates. You just trust Cloud to update the docs for her.

23:41 >> Yeah.

23:42 >> I I do the same. Yeah. I I like I Yeah. I I don't I don't Yeah. So this is like this old versus new paradigm of engineering. Like yes, you have old school engineers that don't use AI, but let's talk about the engineers that use AI to write code in cursor or something like that, but they all want to see the code. Like if anything changes, they're like I better see the changes and approve every single change and and there's this new wave where like I'm at at least at and like lots of others too, but like it's it's a little bit more of like I trust you. I don't need to look at all the codes. I don't need to read all the code but I have systems and

24:25 >> um ways I work with AI that I trust and through that I can let AI do things and I I think with documentation like that is is the same.

24:33 >> Yeah, documentation doesn't affect the product. So it's just docs. Yeah. So

24:37 >> yeah, it's docs. But I I want to say I do the same for like even for product like I do look at all the code that I do for Kora for example because thousands of people use it but

24:47 >> if I vibe code something myself or some something experimental or maybe a part in Kora that is just for me to experiment for now like I don't look at all the code all the time because that's not the point if you

25:01 >> that ruins the vibes man if you keep looking at all the code. I know it ruins the vibes and also that's the whole point of compound engineering is to make sure that if you look at the code and you find something that you make sure

25:12 >> that you will teach it so that next time you don't have to look at the code. So it's capturing

25:18 >> however you work really.

25:21 >> Yeah.

25:21 >> Uh and to make sure Yeah. that that is always working. Okay. So now uh we compounded here and

25:28 yeah we can we can do work. So

25:37 we'll do that. So it compounded that. Um

25:41 now the next step is to do the work uh which is just letting it rip. Um

25:49 >> and obviously it changed the plan now with with the single uh the single tool call. So update settings is now uh you can do as many iterations here as you want obviously but I feel confident now that uh yeah this this is the way I want to go.

26:06 >> Okay.

26:07 >> So if you're very lazy like me, you don't even compact or create a new session. But probably that's better. So let's just do the the better way. So let's do new here. So we clear our session. We have a clear uh

26:24 >> clear context.

26:25 >> Yeah,

26:26 >> clear context because it's all captured in the plan really. So uh we go workflows work and then we paste in the plan. And I use markdown, but uh you don't need to use markdown.

26:40 >> Yeah.

26:40 >> Yeah. You can use GitHub or linear or whatever you want. uh and if you have a GitHub CLI installed, it will pull from GitHub if you have the the linear integration somehow like it will pull from there. So you can you can find a place wherever you want to live. So if you're more if you're a GitHub focused shop or engineer or whatever, then

27:01 >> just do it there.

27:02 >> So what's the difference between like the this this work step versus just you saying let it rip or like go build it? [laughter]

27:12 >> Yeah. You ask you a few questions?

27:13 >> Yeah. Yeah. Yeah. Yeah. So, so yeah, like clearly you can say just do it or something like that. But there is one thing in the beginning here, especially since you have a new fresh uh context here. It will like figure out um if anything is missing because sometimes things are missing. So now it it says I have a few questions. So the plan shows updating user and account in a transaction. uh if only name or time has changed should still wrap a transaction or is it also changed? Well, that's I mean that's a good question and we didn't really answer it in the research.

27:51 Yeah, like sometimes there are good questions um where it's not super well defined. you miss something or it it removes something but

28:01 >> generally uh it yeah it just goes but it does make it does make a plan now how to tackle this so it is a little bit more than just do it it does build a plan how to do this uh let's go I'll I'll just say let's go you figure it out just do the best

28:21 >> and that is fine sometimes and just having these questions here is good for context because it will start thinking about these things and why it is best. So, uh that's why like this is kind of like thinking mode basically but it's like us pushing it to think or like what could go wrong and then it will think oh that could go wrong and then it starts thinking about how it could go right. So it's like traditional prompt engineering

28:48 uh here that just works for you if you

28:51 >> yeah have these tokens.

28:53 >> Dude, it really feels like Yeah, it really feels like you're like a tech lead or like a EM managing like this engineer and you're just having like meetings with it, right? You're just like reviewing his plans.

29:03 >> Yeah, absolutely.

29:04 >> Directions.

29:05 >> Yeah.

29:05 >> Yeah. Yeah. Yeah, I I I think last time we talked about it as well, but like like skills you need are like tech lead skills and like uh management skills. Uh because you're managing these agents and this actually feels like feels very hands-on still. We have to still do all of these things.

29:24 >> Yeah,

29:24 >> I think the future uh and we're very near is where you just do one thing at the start and you get the end result and it's pretty good. And obviously you need to do the compound loop for a little bit. So you need to train it and but it's similar to onboarding a person on on your team. You need to like get them on board, get them used to your code. But once that is done, uh yeah, you can let them go and really uh yeah, really just run with it and uh do more end to end.

29:53 >> Okay, so looks like it's almost done. It's running test already.

29:55 >> Yeah, like this is it. It did the feature and it's writing the test. So uh that's really cool. and and and after that uh one of the coolest things of Opus 4.5 is the testing because it's really good at using playrights and really good at understanding flows. Uh, so this [snorts] I love like before I still had to go in and manually test things. Uh, like clicking on things like obviously writing test it was good at but now we can have playright work. Like it never worked really well but with Opus 4.5 is the first model where I think playright really works. It's not super fast but it works well.

30:35 >> And uh, playright just for audience is like basically like a MCP to have Claude see the browser right? See the browser.

30:42 Yes. Yeah. It's just a Chrome uh like you link Chrome to CL code and like it can control your Chrome window. There is a Chrome plugin for CL code as well which you can use too and that's pretty good. But for me I I like playright a little bit more since yeah you can record the screen you can take screensh I do things like that where I

31:07 >> record the whole video of the whole flow and put it to the pull request automatically as well. So I just like playright a little bit more but whatever works for you if if you like uh to use something else that's

31:18 >> so so basically so basically to use playright you just type one line to install it right and then you just do playright test and what what it's doing right now is uh is loading a browser behind the scenes and playing with the product.

31:29 >> Yeah. So it's now it's still actually it's it's fixing the test still but uh after we can just yeah okay let's say the feature is done uh these

31:39 >> I I think it will work because these are just tests it writing for specific use cases but

31:45 >> yeah we don't

31:46 >> who needs it I I I need test

31:49 >> but just for like us we're very

31:54 >> uh we want to see it we're too excited

31:57 um So you run playright test and what this command will do this is also part of the combat engineering plug-in. It

32:04 will write a plan of like what are the features introduced in in here

32:11 just keeps going. Okay. Well that's good. Yeah. Writes a plan like what to test, what is new, what is introduced. And then um here let's let's just say for now skip the test and go test and play. Right. We'll get back to that after. So you can see how good Opus is with following directions like the we have the Rolf Wigum loop thingy go viral but I haven't seen it to be very very needed because it's pretty good at following

32:41 >> directions. Okay, so here we go. Uh it's funny because it's now

32:47 on deaf please.

32:51 >> Okay, so yeah, so we're here and now it's going to control the screen. So, I will just move this a little bit. Yeah, it's going. So, it's controlling it. It's taking screenshots and it can do all of this. No hands here. Look, it's not me. And it's just testing the feature.

33:07 >> Okay. So, it's kind of like a it's kind of like a browser use thing, right? It's kind of

33:11 >> it's a browser use thing. But the beauty is that this was kind of a missing piece. Like you have system or integration tests obviously, but this is like the ultimate test whether something works. uh- which is like does it work? And it's very easy. You don't even need to write a test and it's not no overhead in like your CI or anything. You just say yo just test it. It's like a QA team basically.

33:37 >> And it's very nice and and you can say just do this for an hour. Think of everything that can go wrong and really kick the tires and like try to break it and it will try to do it. And the beauty is it is in cold code. So if something breaks, it can fix it immediately and immediately validate whether it fixed it. So

33:58 >> it's like this iteration loop using this is very very cool and very very powerful and

34:05 >> and if something uh if something like breaks can can also inspect and see all the console er errors and stuff.

34:11 >> Yes. Yeah. It can control the entire browser. So it can click on elements, it can run JavaScript, it can read the console log. So basically you as an engineer in Chrome it can do everything. So it's it's really cool and also one added thing is like Kora connects to Gmail and and I was doing a feature where uh I just I just launched it where we do email signatures and drafts and to see if that works you need to go to Gmail and how do you write a system integration test to go to Gmail? You're not doing that. But with Payrite, I could just log in with my Gmail account and say, "Hey, I'm logged in with my Gmail account. Just see if it works." And it went to Gmail like it's just a browser. So it's it's it's magical to see it work. Well, it works. Our feature works.

34:58 >> Yeah.

34:58 >> Um which is cool. Um so this is a good state but what I always do after that is uh making sure there are no security risks or if there's no slop or if it looks can be done more simple like there are all these things that can always be better

35:19 >> and uh the review command which is the the last command or it's the it's it's the command we didn't use yet we used the compound already

35:28 >> this is the assess stage right

35:30 >> yeah is the assess state. Yeah. [snorts] stage and it's running reviews from certain perspectives and it's my perspective. So I have an agent that has my like way of working. I added a security person architecture code simplicity reviewer which is also a very good one. uh which like uh

35:54 >> yeah Boris has the has one too and he shared it uh I think this morning on X

36:00 >> so Anthropic does it too

36:03 um like there's also one that reviews whether this is agent native enough dhh is the creator of reals and he will just like he has a very opinionated uh view on things which is hilarious always uh and the beauty is that all these things



36:21 are synthesized into kind of a story to me. So, like, imagine if you have a security reviewer, an architecture reviewer, and a code simplicity reviewer, and they all look at the code and give their feedback. The beauty is that all these things together are synthesized into kind of a story to me. Like, it's not just like, oh, this is wrong, but it's like, oh, this is how we can make it better, and this is the trade-off, and this is why we should do it this way. And that is just so much more valuable than just like a linter or something like that.



37:03 >> Yeah.



37:03 >> So, uh, yeah, this is what I do. And then, uh, if there's feedback, I can either say, uh, fix it or I can say, uh, I'm going to compound it. And then it will be captured and next time it will be better. So, uh, that's the assess phase.



37:22 >> And, and, and this is all automated, right? Like you just run /review and it just does all of this.



37:27 >> Yeah. Yeah. So, uh, you can see here, it's like, uh, it's running the reviews. And, uh, yeah, it's, it's, it's all automated. And, uh, I can just say, uh, fix it or compound it. And, uh, that's it.



37:45 >> That's amazing.



37:46 >> Yeah. So, uh, that's the assess phase. And then, uh, the last phase is compound, which we already did. So, uh, that's the four phases. And, uh, that's really the, the, the whole system.



38:02 >> Yeah. I love it. Um, so, so we have, we have about 10 minutes left. Is there anything else you want to show or, or talk about?



38:09 >> Uh, yeah. So, uh, I want to show the LFG command, which is, uh, the, the, the command that just does everything. So, uh, let's, let's do that. So, uh, I'm going to say, uh, LFG. And, uh, what this does is, uh, it just runs the entire workflow. So, uh, it will plan, it will work, it will assess, and it will compound. And, uh, it just does it. So, uh, you don't even need to understand what all the steps are. Uh, because I think that's going to be interesting and very helpful soon as well.



38:51 >> Yeah.



38:52 >> So, uh, let's, let's see what it does. So, uh, it's, it's starting now. And, uh, it's going to run for about an hour. And, uh, it's going to do everything. So, uh, testing, creating a video, creating a pull request, and it just runs for an hour and it does it.



39:15 >> That's amazing. Um, and, and, and so, so this is like the, the, the future, right? Like you just say one thing and it's done.



39:23 >> Yeah. Yeah. So, uh, that's, that's really the goal. And, uh, I think we're very near. Uh, obviously you need to do the compound loop for a little bit. So you need to train it. But, uh, once that is done, uh, yeah, you can let them go and really, uh, yeah, really just run with it.



39:46 >> That's amazing. Um, I, I, I have one more question. Um, so, so what about slash commands versus sub-agents versus skills? Like when do you use each?



40:00 >> Yeah. Yeah. So, uh, that's a good question. So, uh, slash commands are, are like, uh, the, the, the entry points. So, uh, like /plan, /work, /assess, /compound, /lfg. Those are slash commands. And, uh, they are just, uh, entry points to, to, to the system. And, uh, sub-agents are, are like, uh, the, the, the workers. So, uh, like the best practices researcher, the framework researcher, the spec flow analyzer. Those are sub-agents. And, uh, they do the actual work. And, uh, skills are, are like, uh, the, the, the knowledge. So, uh, like the agent native architecture skill, or, uh, any skill that you create. And, uh, they are just-in-time context. So, uh, whenever you need it, it will pull in that skill file.



41:12 >> Got it. So, so slash commands are like the triggers, sub-agents are like the workers, and skills are like the knowledge.



41:19 >> Yeah. Exactly. Exactly.



41:21 >> That's, that's a great way to think about it. Um, and, and, and so, so, so skills are like, uh, they're not always in context, right? Like they're only pulled in when needed.



41:31 >> Yeah. Yeah. So, uh, that's, that's the beauty of it. Like, uh, if you load all of the skill in context, you would just kill your context. But, uh, with skills, it's just-in-time. So, uh, whenever you need it, it will pull it in.



41:48 >> That's amazing. Um, and, and, and so, so, so how do you create a skill?



41:53 >> Yeah. So, uh, there's a, there's a skill create agent skill in the compound engineering plugin. And, uh, you can just use that. And, uh, it will create a skill for you. And, uh, you can just put all the information in there. And, uh, then you can reference it.



42:15 >> Got it. So, so you don't handwrite skills.



42:18 >> No. No. Yeah. So, uh, there's a, there's a skill for that. And, uh, yeah, don't handwrite skills. But, uh, make sure to read them and review them.



42:29 >> Got it. Um, and, and, and so, so, so when would you use a skill versus just putting something in claude.md?



42:38 >> Yeah. So, uh, claude.md is, is like, uh, the, the, the global context. So, uh, anything that's in there will always be in the prompt. And, uh, skills are, are like, uh, just-in-time context. So, uh, if it's something that's always relevant, put it in claude.md. If it's something that's only relevant for specific tasks, put it in a skill.



43:09 >> Got it. That makes sense. Um, and, and, and so, so, so, so you, you mentioned the LFG command. Like, like, what, what's, what's the, the, the most impressive thing you've done with the LFG command?



43:22 >> Yeah. So, uh, I, I, I have this command now. And, uh, everything we just did, testing and creating a video and creating a pull request, and it just runs for an hour and it does it. So, uh, that's, that's really cool. And, uh, I, I, I think the, the most impressive thing is, uh, just the, the, the fact that it can do end-to-end. Like, uh, from, from zero to production in one command.



43:56 >> That's amazing. Um, and, and, and so, so, so what's, what's next for you? Like, what's, what's, what's the, the next thing you're working on?



44:05 >> Yeah. So, uh, I'm, I'm, I'm really focused on, on Kora right now. And, uh, making it agent native. And, uh, I think that's, that's really the future. Like, uh, agents that can do everything that users can do. And, uh, I'm, I'm really excited about that.



44:26 >> That's amazing. Um, and, and, and so, so, so for people who want to learn more, like, where can they find you?



44:33 >> Yeah. So, uh, I'm on X. Uh, my handle is @kieranklaassen. And, uh, I have a website, cora.computer. And, uh, the GitHub repo for the compound engineering plugin is, uh, github.com/EveryInc/compound-engineering-plugin.



44:55 >> Amazing. Well, thank you so much, Kieran. This was, this was incredible.



44:59 >> Yeah. Thank you so much for having me. It was really fun.



45:02 >> Yeah. And, and for everyone watching, uh, check out the takeaways at creatoreconomy.so. And, uh, yeah, thanks again, Kieran.
