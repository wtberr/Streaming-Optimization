import requests
import random
from datasets import load_dataset

# Hugging Face API URL and Token
API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": "Bearer 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"}


# Function to generate a recommendation for a given movie
def generate_recommendation(movie_title):
    prompt = f"Give me a short recommendation for the movie '{movie_title}' as if you're a friend recommending it."
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    result = response.json()

    # Extract the text from the model response
    return result[0]['generated_text'].strip().lower()


# Create a dictionary with movie titles and corresponding recommendations
def create_movie_recommendation_dict(movie_titles):
    movie_dict = {}
    random_movies = random.sample(movie_titles, 100)  # Randomly pick 100 unique movie titles
    for movie in random_movies:
        recommendation = generate_recommendation(movie)
        movie_dict[movie] = recommendation
    return movie_dict


# OMDb API key
OMDB_API_KEY = 'ab4301c4'


# Function to fetch movie data and create the combined string without labels, punctuation, or capitalization
def get_movie_data(movie_title, movie_recommendations):
    """Fetch movie data and return a continuous string of plot, actors, director, writer, and production."""
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    movie_data = response.json()

    if movie_data['Response'] == 'True':
        # Extract fields, remove punctuation, convert to lowercase
        plot = movie_data.get('Plot', '').lower()
        actors = movie_data.get('Actors', '').lower()
        director = movie_data.get('Director', '').lower()
        writer = movie_data.get('Writer', '').lower()
        production = movie_data.get('Production', '').lower()
        genre = movie_data.get('Genre', '').split(', ')

        # Combine all the elements into a string without labels or punctuation
        combined_info = f"{plot} {actors} {director} {writer} {production}".replace(',', '')
        return [movie_recommendations[movie_title], combined_info.strip(), genre]  # Remove any extra spaces
    else:
        return f"Error: {movie_data.get('Error', 'Unknown error occurred')}"


# Create a dictionary for the movies with recommendations, continuous string, and genres
def create_movies_dict():
    # Load the dataset
    ds = load_dataset("wykonos/movies", split='train[:500]')

    # Extract movie titles from the dataset
    movie_titles = [item['title'] for item in ds]  # Assuming 'title' is the field name for the movie title

    # Generate the dictionary of recommendations
    movie_recommendations = create_movie_recommendation_dict(movie_titles)

    movies_dict = {}

    # Loop through the movie recommendations and populate the dictionary
    for movie in movie_recommendations:
        movies_dict[movie] = get_movie_data(movie, movie_recommendations)

    return movies_dict


# Example movie dictionary with movie names, recommendations, overviews, and genres
movies = {
    "Breaking Bad": [
        "You have to watch Breaking Bad, it's one of the best shows out there! The character development is insane!",
        "Breaking Bad is a story about a high school chemistry teacher, Walter White, who turns to cooking methamphetamine after being diagnosed with terminal cancer. The series follows his descent into the criminal underworld as he partners with former student Jesse Pinkman, balancing family life with his new dangerous endeavors. Directed by Vince Gilligan, starring Bryan Cranston, Aaron Paul, and Anna Gunn. Produced by Sony Pictures Television. It was critically acclaimed.",
        ["Drama", "Crime"]
    ],
    "Friends": [
        "It's a light-hearted, feel-good sitcom about a group of friends living in New York City.",
        "Friends follows six individuals—Monica, Chandler, Joey, Ross, Rachel, and Phoebe—as they navigate life, relationships, and careers in New York City. Directed by David Crane and Marta Kauffman, starring Jennifer Aniston, Courteney Cox, and Matthew Perry. Produced by Warner Bros. Television. It was critically acclaimed.",
        ["Comedy"]
    ],
    "The X-Files": [
        "If you love sci-fi and mystery, The X-Files is a must! It blends supernatural mysteries with detective work.",
        "The X-Files revolves around FBI agents Fox Mulder and Dana Scully as they investigate unsolved, often paranormal cases known as X-Files. Mulder believes in extraterrestrial and supernatural phenomena, while Scully, a medical doctor, is more skeptical and analytical. Directed by Chris Carter, starring David Duchovny and Gillian Anderson. Produced by 20th Century Fox Television. It was critically acclaimed.",
        ["Sci-Fi", "Mystery"]
    ],
    "The Sopranos": [
        "The Sopranos is a deep dive into the life of a mob boss with a psychological twist. Highly recommended!",
        "The Sopranos follows Tony Soprano, a mob boss trying to balance the demands of his crime family with the complexities of his personal life. The show explores themes of crime, family, and mental health. Directed by David Chase, starring James Gandolfini, Lorraine Bracco, and Edie Falco. Produced by HBO. It was critically acclaimed.",
        ["Drama", "Crime"]
    ],
    "Game of Thrones": [
        "One of the best fantasy series ever made! The twists and turns will keep you hooked.",
        "Based on George R.R. Martin’s 'A Song of Ice and Fire' series, Game of Thrones follows the political and military struggles between noble families in the fictional continents of Westeros and Essos as they vie for control of the Iron Throne and ultimate power over the Seven Kingdoms. Directed by David Benioff and D.B. Weiss, starring Emilia Clarke, Kit Harington, and Lena Headey. Produced by HBO. It was critically acclaimed.",
        ["Fantasy", "Drama"]
    ],
    "Stranger Things": [
        "A great mix of 80s nostalgia, sci-fi, and horror with a lovable group of kids battling supernatural forces!",
        "Set in the 1980s, Stranger Things follows a group of kids who uncover dark government secrets and face terrifying supernatural creatures after their friend goes missing. The show is filled with pop-culture references and thrilling mystery. Directed by The Duffer Brothers, starring Millie Bobby Brown, Finn Wolfhard, and Winona Ryder. Produced by Netflix. It was critically acclaimed.",
        ["Sci-Fi", "Horror"]
    ],
    "The Office (US)": [
        "One of the funniest workplace comedies ever, with some of the most memorable characters in TV history!",
        "The Office is a mockumentary-style sitcom that depicts the everyday lives of office employees working at Dunder Mifflin's Scranton, Pennsylvania branch. The show features a quirky cast led by the well-meaning but often clueless boss Michael Scott. Directed by Greg Daniels, starring Steve Carell, Rainn Wilson, and John Krasinski. Produced by NBC. It was critically acclaimed.",
        ["Comedy"]
    ],
    "Mad Men": [
        "If you're into deep character development and the 1960s, Mad Men is a fantastic period drama.",
        "Mad Men is set in the 1960s and follows the lives of the employees at a prestigious advertising agency in New York City. The show focuses particularly on Don Draper, a talented but troubled advertising executive. Directed by Matthew Weiner, starring Jon Hamm, Elisabeth Moss, and Vincent Kartheiser. Produced by Lionsgate Television. It was critically acclaimed.",
        ["Drama"]
    ],
    "The Simpsons": [
        "It's one of the most iconic animated series ever, and it's still going strong!",
        "The Simpsons is an animated sitcom following the Simpson family in the fictional town of Springfield. The show satirizes American culture, politics, and society through the misadventures of Homer, Marge, Bart, Lisa, and Maggie. Created by Matt Groening, starring Dan Castellaneta, Julie Kavner, and Nancy Cartwright. Produced by 20th Century Fox Television. It was critically acclaimed.",
        ["Animation", "Comedy"]
    ],
    "Doctor Who": [
        "A classic sci-fi show about time travel and adventure across the universe.",
        "Doctor Who follows the Doctor, a time-traveling alien Time Lord from the planet Gallifrey, as they travel across time and space to fight evil forces. The Doctor often regenerates into a new form, taking on new companions and enemies. Created by Sydney Newman, starring various actors as the Doctor over time, including Jodie Whittaker and David Tennant. Produced by BBC. It was critically acclaimed.",
        ["Sci-Fi"]
    ],
    "The Wire": [
        "A groundbreaking series that explores the drug trade, law enforcement, and life in Baltimore.",
        "The Wire is a gritty, realistic portrayal of life in Baltimore, focusing on the intersection of law enforcement, drug dealers, and residents caught in the crossfire. Each season focuses on different aspects of the city's struggles. Directed by David Simon, starring Dominic West, Lance Reddick, and Sonja Sohn. Produced by HBO. It was critically acclaimed.",
        ["Crime", "Drama"]
    ],
    "Seinfeld": [
        "A classic sitcom about nothing! It's one of the funniest shows ever made.",
        "Seinfeld follows the life of comedian Jerry Seinfeld and his quirky group of friends in New York City. The show focuses on the minutiae of everyday life, often to hilarious effect. Created by Jerry Seinfeld and Larry David, starring Jerry Seinfeld, Julia Louis-Dreyfus, and Jason Alexander. Produced by Castle Rock Entertainment. It was critically acclaimed.",
        ["Comedy"]
    ],
    "Sherlock": [
        "Sherlock is a brilliant modern adaptation of the classic detective stories.",
        "Sherlock follows a modern-day version of Sherlock Holmes as he solves complex crimes in London, assisted by his friend Dr. John Watson. The show combines mystery with character-driven drama. Directed by Steven Moffat and Mark Gatiss, starring Benedict Cumberbatch and Martin Freeman. Produced by Hartswood Films. It was critically acclaimed.",
        ["Mystery", "Crime"]
    ],
    "Buffy the Vampire Slayer": [
        "A fun mix of action, fantasy, and drama as Buffy fights vampires and other supernatural foes.",
        "Buffy the Vampire Slayer follows Buffy Summers, a high school student chosen to fight vampires, demons, and other supernatural creatures. The show balances action, supernatural lore, and character relationships. Directed by Joss Whedon, starring Sarah Michelle Gellar, Alyson Hannigan, and Nicholas Brendon. Produced by 20th Century Fox Television. It was critically acclaimed.",
        ["Fantasy", "Action"]
    ],
    "Lost": [
        "Lost is an adventure mystery that will keep you guessing with its twists and turns.",
        "Lost follows the survivors of a plane crash as they are stranded on a mysterious island filled with secrets and strange occurrences. The series weaves a complex narrative involving time travel, mysterious organizations, and deep character exploration. Directed by J.J. Abrams, Damon Lindelof, and Jeffrey Lieber, starring Matthew Fox, Evangeline Lilly, and Terry O'Quinn. Produced by ABC Studios. It was critically acclaimed.",
        ["Adventure", "Mystery"]
    ],
    "Grey's Anatomy": [
        "If you like medical dramas, Grey's Anatomy is a solid pick with a ton of seasons to binge!",
        "Grey's Anatomy focuses on the lives of surgical interns and residents as they evolve into seasoned doctors while trying to maintain personal lives. The show is known for its dramatic, romantic, and emotional storylines. Created by Shonda Rhimes, starring Ellen Pompeo, Sandra Oh, and Patrick Dempsey. Produced by ABC Studios. It was critically acclaimed.",
        ["Medical Drama"]
    ],
    "Parks and Recreation": [
        "A hilarious mockumentary-style show about quirky government employees in a small town.",
        "Parks and Recreation follows the enthusiastic and optimistic Leslie Knope, a mid-level bureaucrat in the Parks Department of the fictional town of Pawnee, Indiana, as she navigates the challenges of government work with her unique group of co-workers. Directed by Michael Schur and Greg Daniels, starring Amy Poehler, Nick Offerman, and Rashida Jones. Produced by NBC. It was critically acclaimed.",
        ["Comedy"]
    ],
    "House": [
        "A medical drama with a brilliant but abrasive doctor solving complex cases.",
        "House follows Dr. Gregory House, a misanthropic genius diagnostician with a knack for solving difficult medical cases. His unorthodox methods and anti-social behavior lead to tension with his colleagues. Directed by David Shore, starring Hugh Laurie, Omar Epps, and Robert Sean Leonard. Produced by Fox. It was critically acclaimed.",
        ["Medical Drama"]
    ],
    "Supernatural": [
        "A long-running show about two brothers hunting monsters, demons, and ghosts.",
        "Supernatural follows brothers Sam and Dean Winchester as they hunt supernatural creatures including demons, ghosts, and gods, all while uncovering family secrets and dealing with cosmic forces. Directed by Eric Kripke, starring Jared Padalecki, Jensen Ackles, and Misha Collins. Produced by Warner Bros. Television. It was critically acclaimed.",
        ["Fantasy", "Horror"]
    ],
    "Black Mirror": [
        "A chilling anthology series exploring the dark side of technology.",
        "Black Mirror is an anthology series that examines modern society, particularly with regard to the unanticipated consequences of new technologies. Each episode stands alone and explores themes of dystopia, human nature, and technology. Directed by Charlie Brooker, starring various actors across different episodes. Produced by Netflix. It was critically acclaimed.",
        ["Sci-Fi", "Anthology"]
    ],
    "Fargo": [
        "A dark, witty crime series with interconnected stories.",
        "Inspired by the Coen brothers' film of the same name, Fargo presents interconnected tales of crime, greed, and human nature in the American Midwest. Each season stands alone, featuring different characters and stories. Directed by Noah Hawley, starring Billy Bob Thornton, Martin Freeman, and Allison Tolman. Produced by FX. It was critically acclaimed.",
        ["Crime", "Drama"]
    ],
    "True Detective": [
        "A gripping crime anthology with incredible performances.",
        "True Detective is a crime anthology series, with each season featuring a new cast and storyline. The show explores dark themes of crime, morality, and human nature. Directed by Nic Pizzolatto, starring Matthew McConaughey, Woody Harrelson, and Mahershala Ali. Produced by HBO. It was critically acclaimed.",
        ["Crime", "Drama"]
    ],
    "How I Met Your Mother": [
        "A comedy about friendships and romance in New York City, told with a unique twist.",
        "How I Met Your Mother is a sitcom that follows Ted Mosby as he tells his children the story of how he met their mother, recounting his adventures with his quirky group of friends along the way. Directed by Carter Bays and Craig Thomas, starring Josh Radnor, Jason Segel, and Cobie Smulders. Produced by CBS. It was critically acclaimed.",
        ["Comedy", "Romance"]
    ],
    "The Crown": [
        "A stunning historical drama about the reign of Queen Elizabeth II.",
        "The Crown chronicles the reign of Queen Elizabeth II, exploring the political and personal events that shaped the second half of the 20th century in Britain. The show delves into the pressures of royalty and the complexities of leadership. Directed by Peter Morgan, starring Claire Foy, Matt Smith, and Olivia Colman. Produced by Netflix. It was critically acclaimed.",
        ["Historical Drama"]
    ],
    "Westworld": [
        "A mind-bending sci-fi series about a futuristic theme park where robots rebel.",
        "Westworld is a dystopian sci-fi series set in a high-tech theme park where human-like robots cater to the whims of the park's guests. The show explores themes of artificial intelligence, free will, and morality. Directed by Jonathan Nolan and Lisa Joy, starring Evan Rachel Wood, Jeffrey Wright, and Thandiwe Newton. Produced by HBO. It was critically acclaimed.",
        ["Sci-Fi", "Western"]
    ],
    "The West Wing": [
        "A political drama that takes you inside the White House, showing the inner workings of the U.S. government.",
        "The West Wing follows the daily lives of the staffers and advisors of President Josiah Bartlet as they navigate political, personal, and ethical challenges in the White House. Directed by Aaron Sorkin, starring Martin Sheen, Rob Lowe, and Allison Janney. Produced by NBC. It was critically acclaimed.",
        ["Political Drama"]
    ],
    "Arrested Development": [
        "A quirky comedy about a dysfunctional wealthy family navigating financial ruin.",
        "Arrested Development follows the Bluth family, once wealthy but now in financial and legal trouble, as they struggle to keep their lives together in hilarious ways. The show is known for its quirky characters and fast-paced humor. Directed by Mitchell Hurwitz, starring Jason Bateman, Michael Cera, and Jessica Walter. Produced by Fox. It was critically acclaimed.",
        ["Comedy"]
    ],
    "Frasier": [
        "A witty and intelligent sitcom about a radio psychiatrist and his eccentric family.",
        "Frasier is a spin-off of Cheers, following Dr. Frasier Crane as he moves back to Seattle to work as a radio psychiatrist and reconnect with his quirky family. The show blends intelligent humor with heartfelt moments. Directed by David Angell, Peter Casey, and David Lee, starring Kelsey Grammer, David Hyde Pierce, and John Mahoney. Produced by NBC. It was critically acclaimed.",
        ["Comedy"]
    ],
    "Curb Your Enthusiasm": [
        "A hilarious, improvised show where Larry David plays an exaggerated version of himself.",
        "Curb Your Enthusiasm follows Larry David, playing a fictionalized version of himself, as he navigates everyday life with his unique sense of humor and often inappropriate behavior. Directed by Larry David, starring Larry David, Cheryl Hines, and Jeff Garlin. Produced by HBO. It was critically acclaimed.",
        ["Comedy"]
    ],
    "The Mandalorian": [
        "A thrilling Star Wars spin-off about a lone bounty hunter in the galaxy.",
        "The Mandalorian follows Din Djarin, a bounty hunter, as he navigates the galaxy while protecting a mysterious child, often referred to as Baby Yoda. The show explores new areas of the Star Wars universe. Directed by Jon Favreau, starring Pedro Pascal, Gina Carano, and Carl Weathers. Produced by Lucasfilm. It was critically acclaimed.",
        ["Sci-Fi", "Adventure"]
    ],
    "The Handmaid's Tale": [
        "A dystopian drama about a totalitarian society where women are oppressed.",
        "The Handmaid's Tale is set in the near future in the dystopian society of Gilead, where fertile women, known as Handmaids, are forced into servitude to bear children for the ruling class. The show explores themes of oppression, freedom, and resistance. Directed by Bruce Miller, starring Elisabeth Moss, Yvonne Strahovski, and Joseph Fiennes. Produced by MGM Television. It was critically acclaimed.",
        ["Dystopian", "Drama"]
    ],
    "Big Little Lies": [
        "A gripping mystery about secrets, lies, and murder in a wealthy seaside town.",
        "Big Little Lies follows a group of women living in a wealthy seaside town, each hiding dark secrets that ultimately lead to murder. The show combines mystery, drama, and strong character development. Directed by Jean-Marc Vallée, starring Reese Witherspoon, Nicole Kidman, and Shailene Woodley. Produced by HBO. It was critically acclaimed.",
        ["Drama", "Mystery"]
    ],
    "The Boys": [
        "A dark and gritty superhero show with a satirical edge.",
        "The Boys takes place in a world where superheroes are controlled by a powerful corporation and often abuse their powers. A group of vigilantes known as 'The Boys' set out to expose the truth about the so-called heroes. Directed by Eric Kripke, starring Karl Urban, Jack Quaid, and Antony Starr. Produced by Amazon Studios. It was critically acclaimed.",
        ["Superhero", "Comedy"]
    ],
    "BoJack Horseman": [
        "An animated comedy that offers a satirical and poignant look at fame and mental health.",
        "BoJack Horseman is an animated series about a washed-up actor, who happens to be a horse, as he struggles with his career, relationships, and mental health. The show blends dark humor with emotional storytelling. Directed by Raphael Bob-Waksberg, starring Will Arnett, Alison Brie, and Aaron Paul. Produced by Netflix. It was critically acclaimed.",
        ["Animation", "Comedy"]
    ],
    "The Marvelous Mrs. Maisel": [
        "A fantastic, vibrant comedy about a woman finding her voice in stand-up comedy in the 1950s.",
        "The Marvelous Mrs. Maisel follows Miriam 'Midge' Maisel, a 1950s housewife in New York City who discovers she has a knack for stand-up comedy. The series is filled with quick wit, period-accurate settings, and strong performances. Directed by Amy Sherman-Palladino, starring Rachel Brosnahan, Tony Shalhoub, and Alex Borstein. Produced by Amazon Studios. It was critically acclaimed.",
        ["Comedy", "Drama"]
    ],
    "Succession": [
        "A sharp, tense drama about a dysfunctional wealthy family vying for control of their media empire.",
        "Succession follows the power struggles within the Roy family, owners of a global media conglomerate, as the aging patriarch considers his succession plan. The show delves into themes of greed, power, and familial betrayal. Directed by Jesse Armstrong, starring Brian Cox, Jeremy Strong, and Sarah Snook. Produced by HBO. It was critically acclaimed.",
        ["Drama"]
    ],
    "Better Call Saul": [
        "A fantastic prequel to Breaking Bad, focusing on the transformation of Jimmy McGill into Saul Goodman.",
        "Better Call Saul tells the story of Jimmy McGill, a small-time lawyer who gradually transforms into the morally dubious lawyer Saul Goodman. The show offers a slow-burn character study with compelling legal drama. Directed by Vince Gilligan and Peter Gould, starring Bob Odenkirk, Jonathan Banks, and Rhea Seehorn. Produced by AMC. It was critically acclaimed.",
        ["Drama", "Crime"]
    ],
    "30 Rock": [
        "A fast-paced, witty comedy about the behind-the-scenes antics of a fictional TV show.",
        "30 Rock is a satirical sitcom that follows Liz Lemon, the head writer of a fictional live sketch-comedy show, as she deals with her eccentric boss and unpredictable cast. The show is filled with sharp humor and industry satire. Directed by Tina Fey, starring Tina Fey, Alec Baldwin, and Tracy Morgan. Produced by NBC. It was critically acclaimed.",
        ["Comedy"]
    ],
    "Rick and Morty": [
        "An offbeat, smart, and often dark animated series about a mad scientist and his adventures with his grandson.",
        "Rick and Morty follows the misadventures of an eccentric and alcoholic scientist, Rick, and his good-hearted but easily influenced grandson, Morty, as they travel through alternate dimensions and experience bizarre, often dangerous, adventures. Created by Justin Roiland and Dan Harmon, starring Justin Roiland, Chris Parnell, and Spencer Grammer. Produced by Adult Swim. It was critically acclaimed.",
        ["Animation", "Sci-Fi"]
    ],
    "Narcos": [
        "A gripping crime drama that chronicles the rise of the drug trade and the people trying to stop it.",
        "Narcos tells the true-life story of the growth of cocaine cartels across Colombia and the gripping real-life stories of drug lords like Pablo Escobar, as well as the DEA agents tasked with bringing them down. Directed by Chris Brancato, Carlo Bernard, and Doug Miro, starring Wagner Moura, Pedro Pascal, and Boyd Holbrook. Produced by Netflix. It was critically acclaimed.",
        ["Crime", "Drama"]
    ],
    "Peaky Blinders": [
        "A slick, stylish drama about a crime family in post-World War I England.",
        "Peaky Blinders follows the Shelby family, a powerful crime gang in post-World War I Birmingham, England, as they navigate politics, rival gangs, and personal struggles. The show is known for its striking visuals, excellent writing, and complex characters. Directed by Steven Knight, starring Cillian Murphy, Paul Anderson, and Helen McCrory. Produced by BBC. It was critically acclaimed.",
        ["Crime", "Drama"]
    ],
    "Schitt's Creek": [
        "A heartwarming and hilarious comedy about a wealthy family that loses everything and has to start over in a small town.",
        "Schitt's Creek follows the Rose family, who lose their fortune and are forced to live in a small town they once bought as a joke. The show is filled with quirky characters and heartfelt moments. Directed by Dan Levy and Eugene Levy, starring Eugene Levy, Catherine O'Hara, and Dan Levy. Produced by Not A Real Company Productions. It was critically acclaimed.",
        ["Comedy"]
    ],
    "Brooklyn Nine-Nine": [
        "A hilarious, light-hearted police procedural comedy with a fantastic ensemble cast.",
        "Brooklyn Nine-Nine follows the detectives of the NYPD's 99th precinct as they solve crimes, navigate their quirky personal lives, and deal with their eccentric captain. Directed by Michael Schur and Dan Goor, starring Andy Samberg, Terry Crews, and Andre Braugher. Produced by NBC. It was critically acclaimed.",
        ["Comedy", "Crime"]
    ],
    "The Expanse": [
        "A complex and engaging sci-fi series set in a future where humanity has colonized the solar system.",
        "The Expanse is set hundreds of years in the future, where humanity has colonized the solar system. It follows a group of unlikely heroes as they unravel a vast conspiracy that threatens peace between Earth, Mars, and the Belt. Directed by Mark Fergus and Hawk Ostby, starring Steven Strait, Dominique Tipper, and Wes Chatham. Produced by Amazon Studios. It was critically acclaimed.",
        ["Sci-Fi", "Drama"]
    ],
    "Downton Abbey": [
        "A beautifully crafted historical drama about the lives of the aristocratic Crawley family and their servants.",
        "Downton Abbey follows the lives of the aristocratic Crawley family and their servants in the early 20th century. The series explores social changes, romance, and the relationships between the family and their household staff. Directed by Julian Fellowes, starring Hugh Bonneville, Michelle Dockery, and Maggie Smith. Produced by ITV. It was critically acclaimed.",
        ["Historical Drama"]
    ],
    "The Walking Dead": [
        "A gripping and intense zombie apocalypse drama that explores survival, human nature, and community.",
        "The Walking Dead follows a group of survivors as they navigate a post-apocalyptic world overrun by zombies. The show explores themes of survival, human nature, and the collapse of civilization. Directed by Frank Darabont, starring Andrew Lincoln, Norman Reedus, and Melissa McBride. Produced by AMC. It was critically acclaimed.",
        ["Horror", "Drama"]
    ],
    "Orange Is the New Black": [
        "A darkly comedic drama set inside a women's prison, exploring issues of race, class, and identity.",
        "Orange Is the New Black follows Piper Chapman, a woman sentenced to prison for a crime she committed years ago. The show blends humor and drama as it explores the lives of the inmates in the women's prison system. Directed by Jenji Kohan, starring Taylor Schilling, Laura Prepon, and Uzo Aduba. Produced by Netflix. It was critically acclaimed.",
        ["Comedy", "Drama"]
    ],
    "Vikings": [
        "A historical drama that follows the legendary Viking chieftain Ragnar Lothbrok and his quest for power.",
        "Vikings follows the legendary Norse hero Ragnar Lothbrok as he rises from farmer to king, leading his people in raids and conquest while navigating complex family dynamics and political intrigue. Directed by Michael Hirst, starring Travis Fimmel, Katheryn Winnick, and Clive Standen. Produced by History Channel. It was critically acclaimed.",
        ["Historical", "Drama"]
    ],
    "Atlanta": [
        "A unique and insightful dramedy about a man trying to manage his cousin's rap career in Atlanta.",
        "Atlanta follows Earn, a man who becomes the manager for his cousin, an up-and-coming rapper known as Paper Boi, as they navigate the Atlanta music scene and the complexities of race, poverty, and success. Directed by Donald Glover, starring Donald Glover, Brian Tyree Henry, and Lakeith Stanfield. Produced by FX. It was critically acclaimed.",
        ["Comedy", "Drama"]
    ],
    "It's Always Sunny in Philadelphia": [
        "A dark, hilarious sitcom about a group of morally bankrupt friends running a bar.",
        "It's Always Sunny in Philadelphia follows 'The Gang,' a group of friends who own a bar in Philadelphia and consistently get into ridiculous and unethical situations. The show is known for its dark humor and lack of moral lessons. Directed by Rob McElhenney, starring Charlie Day, Glenn Howerton, and Rob McElhenney. Produced by FX. It was critically acclaimed.",
        ["Comedy"]
    ],
    "Fleabag": [
        "A brilliant, dark comedy that offers a raw and hilarious look at modern life, love, and family.",
        "Fleabag follows a young woman, known only as Fleabag, as she navigates life in London while dealing with family issues, relationships, and grief. The show is filled with dark humor, wit, and deeply emotional moments. Directed by Phoebe Waller-Bridge, starring Phoebe Waller-Bridge, Sian Clifford, and Olivia Colman. Produced by Amazon Studios. It was critically acclaimed.",
        ["Comedy", "Drama"]
    ],
    "Homeland": [
        "A tense and gripping political thriller about the complexities of terrorism, intelligence, and loyalty.",
        "Homeland follows CIA officer Carrie Mathison as she navigates the murky waters of intelligence, counterterrorism, and mental health while trying to stop terrorist threats against the United States. Directed by Alex Gansa and Howard Gordon, starring Claire Danes, Mandy Patinkin, and Damian Lewis. Produced by Showtime. It was critically acclaimed.",
        ["Thriller", "Drama"]
    ],
    "The Americans": [
        "A suspenseful spy drama about two Russian KGB officers posing as an American couple during the Cold War.",
        "The Americans follows Elizabeth and Philip Jennings, two Russian KGB officers posing as a married couple in the United States during the Cold War. The show explores themes of loyalty, identity, and the complexities of espionage. Directed by Joseph Weisberg, starring Keri Russell, Matthew Rhys, and Noah Emmerich. Produced by FX. It was critically acclaimed.",
        ["Spy", "Drama"]
    ],
    "Dexter": [
        "A dark crime drama about a forensic expert who leads a secret life as a vigilante serial killer.",
        "Dexter follows Dexter Morgan, a forensic blood spatter analyst for the Miami police department, who harbors a dark secret—he is also a vigilante serial killer who only kills other murderers. Directed by James Manos Jr., starring Michael C. Hall, Jennifer Carpenter, and David Zayas. Produced by Showtime. It was critically acclaimed.",
        ["Crime", "Thriller"]
    ],
    "True Blood": [
        "A dark and thrilling fantasy about vampires living among humans in a small Louisiana town.",
        "True Blood is set in a world where vampires have 'come out of the coffin' and live openly among humans. The story follows telepathic waitress Sookie Stackhouse as she becomes entangled with vampires, werewolves, and other supernatural beings. Directed by Alan Ball, starring Anna Paquin, Stephen Moyer, and Alexander Skarsgård. Produced by HBO. It was critically acclaimed.",
        ["Fantasy", "Drama"]
    ],
    "The Good Place": [
        "A quirky and philosophical comedy about what happens after you die.",
        "The Good Place follows Eleanor Shellstrop, a woman who finds herself in the afterlife's 'Good Place' by mistake. The series blends humor with deep philosophical questions about ethics, morality, and what it means to be a good person. Directed by Michael Schur, starring Kristen Bell, Ted Danson, and William Jackson Harper. Produced by NBC. It was critically acclaimed.",
        ["Comedy", "Fantasy"]
    ],
    "Deadwood": [
        "A gritty Western drama about power, corruption, and survival in the American frontier.",
        "Deadwood is set in the late 1800s in the town of Deadwood, South Dakota. The series follows the lawless rise of the town as different factions, including criminals, businesspeople, and lawmen, vie for power. Directed by David Milch, starring Timothy Olyphant, Ian McShane, and Molly Parker. Produced by HBO. It was critically acclaimed.",
        ["Western", "Drama"]
    ],
    "Lucifer": [
        "A fun and witty fantasy series about the devil solving crimes in Los Angeles.",
        "Lucifer follows Lucifer Morningstar, the Devil, who becomes bored with Hell and relocates to Los Angeles, where he runs a nightclub and works as a consultant for the LAPD. The show mixes crime-solving with supernatural elements. Directed by Tom Kapinos, starring Tom Ellis, Lauren German, and Kevin Alejandro. Produced by Warner Bros. Television. It was critically acclaimed.",
        ["Fantasy", "Crime"]
    ],
    "This Is Us": [
        "An emotional and heartwarming drama about the lives of a family across several decades.",
        "This Is Us follows the Pearson family across different generations, focusing on themes of love, loss, and personal struggles. The show's unique storytelling format weaves between past, present, and future. Directed by Dan Fogelman, starring Milo Ventimiglia, Mandy Moore, and Sterling K. Brown. Produced by NBC. It was critically acclaimed.",
        ["Drama", "Family"]
    ],
    "Marvel's Daredevil": [
        "A dark and intense superhero series about a blind lawyer who fights crime by night.",
        "Daredevil follows Matt Murdock, a blind lawyer by day and vigilante by night, as he fights crime in Hell's Kitchen, New York. The show blends superhero action with legal drama and intense fight sequences. Directed by Drew Goddard, starring Charlie Cox, Deborah Ann Woll, and Vincent D'Onofrio. Produced by Netflix. It was critically acclaimed.",
        ["Action", "Crime", "Superhero"]
    ],
    "Ozark": [
        "A dark and thrilling drama about a family caught in the web of crime and money laundering.",
        "Ozark follows financial planner Marty Byrde, who relocates his family to the Ozarks after a money-laundering scheme goes wrong. He is forced to work for a Mexican cartel, leading to increasingly dangerous situations. Directed by Bill Dubuque, starring Jason Bateman, Laura Linney, and Julia Garner. Produced by Netflix. It was critically acclaimed.",
        ["Crime", "Drama"]
    ],
    "House of Cards": [
        "A gripping political thriller about power, manipulation, and corruption in Washington D.C.",
        "House of Cards follows the ruthless politician Frank Underwood as he schemes his way to power in Washington, D.C., using manipulation, betrayal, and murder to achieve his goals. Directed by Beau Willimon, starring Kevin Spacey, Robin Wright, and Michael Kelly. Produced by Netflix. It was critically acclaimed.",
        ["Political Drama"]
    ],
    "Battlestar Galactica": [
        "A complex and epic space opera about humanity's survival against a deadly race of robots.",
        "Battlestar Galactica is set in a distant star system where the remnants of humanity are fleeing from the robotic Cylons. The survivors are searching for a new home while dealing with threats from within and without. Directed by Ronald D. Moore, starring Edward James Olmos, Mary McDonnell, and Katee Sackhoff. Produced by Universal Television. It was critically acclaimed.",
        ["Sci-Fi", "Drama"]
    ],
    "American Horror Story": [
        "A dark and terrifying anthology series exploring different horror genres and settings each season.",
        "American Horror Story is an anthology horror series, with each season telling a new story centered on various themes such as haunted houses, witchcraft, and cults. Directed by Ryan Murphy and Brad Falchuk, starring Sarah Paulson, Evan Peters, and Jessica Lange. Produced by FX. It was critically acclaimed.",
        ["Horror", "Anthology"]
    ],
    "The Witcher": [
        "A fantasy epic following a monster hunter as he navigates a war-torn world full of magic and political intrigue.",
        "The Witcher follows Geralt of Rivia, a solitary monster hunter, as he struggles to find his place in a world where people often prove more wicked than the monsters he hunts. The show explores themes of destiny, family, and morality. Directed by Lauren Schmidt Hissrich, starring Henry Cavill, Anya Chalotra, and Freya Allan. Produced by Netflix. It was critically acclaimed.",
        ["Fantasy", "Drama"]
    ],
    "GLOW": [
        "A fun and unique dramedy about female wrestlers in the 1980s.",
        "GLOW follows a group of women in the 1980s as they form a wrestling troupe known as the Gorgeous Ladies of Wrestling. The show mixes humor, drama, and the challenges of breaking into the world of entertainment. Directed by Liz Flahive and Carly Mensch, starring Alison Brie, Marc Maron, and Betty Gilpin. Produced by Netflix. It was critically acclaimed.",
        ["Comedy", "Drama"]
    ],
    "Veep": [
        "A razor-sharp political satire about a woman navigating the chaos of Washington, D.C.",
        "Veep follows Selina Meyer, a former senator who becomes Vice President of the United States, as she navigates the absurdity and dysfunction of American politics. The show is known for its biting satire and fast-paced dialogue. Directed by Armando Iannucci, starring Julia Louis-Dreyfus, Tony Hale, and Anna Chlumsky. Produced by HBO. It was critically acclaimed.",
        ["Political", "Comedy"]
    ],
    "Mindhunter": [
        "A fascinating and chilling crime drama about the early days of criminal profiling at the FBI.",
        "Mindhunter is based on the true story of the FBI's Behavioral Science Unit as they interview notorious serial killers to understand how they think. The show delves into the psychological aspects of crime and the toll it takes on the investigators. Directed by David Fincher, starring Jonathan Groff, Holt McCallany, and Anna Torv. Produced by Netflix. It was critically acclaimed.",
        ["Crime", "Drama"]
    ],
    "Outlander": [
        "A sweeping historical romance with elements of time travel and adventure.",
        "Outlander follows Claire Randall, a married nurse from 1945 who is mysteriously transported back to 1743 Scotland. She becomes embroiled in the Jacobite risings and falls in love with a Highland warrior. Directed by Ronald D. Moore, starring Caitríona Balfe, Sam Heughan, and Tobias Menzies. Produced by Starz. It was critically acclaimed.",
        ["Romance", "Sci-Fi"]
    ],
    "Superstore": [
        "A hilarious workplace comedy set in a big-box retail store.",
        "Superstore follows the employees of Cloud 9, a fictional big-box retail store, as they deal with workplace challenges, relationships, and corporate policies. The show blends humor with commentary on modern work culture. Directed by Justin Spitzer, starring America Ferrera, Ben Feldman, and Mark McKinney. Produced by NBC. It was critically acclaimed.",
        ["Comedy"]
    ],
    "The Good Wife": [
        "A sharp legal drama about a woman who returns to her career as a lawyer after her husband's political scandal.",
        "The Good Wife follows Alicia Florrick, the wife of a disgraced politician, as she rebuilds her career as a defense attorney. The show combines legal drama with political intrigue. Directed by Michelle King and Robert King, starring Julianna Margulies, Matt Czuchry, and Christine Baranski. Produced by CBS. It was critically acclaimed.",
        ["Legal Drama"]
    ],
    "Euphoria": [
        "A bold and intense teen drama exploring addiction, identity, and trauma.",
        "Euphoria follows a group of high school students as they navigate issues such as addiction, mental health, identity, and relationships. The show is known for its raw storytelling and visual style. Directed by Sam Levinson, starring Zendaya, Hunter Schafer, and Jacob Elordi. Produced by HBO. It was critically acclaimed.",
        ["Teen Drama"]
    ],
    "The Haunting of Hill House": [
        "A haunting and emotional horror series about a family's traumatic past and the house that still haunts them.",
        "The Haunting of Hill House follows the Crain family as they confront the trauma caused by their experiences living in a haunted mansion. The show masterfully blends horror with deep emotional storytelling. Directed by Mike Flanagan, starring Michiel Huisman, Carla Gugino, and Elizabeth Reaser. Produced by Netflix. It was critically acclaimed.",
        ["Horror", "Drama"]
    ],
    "Justified": [
        "A modern Western about a U.S. Marshal enforcing justice in his rural Kentucky hometown.",
        "Justified follows U.S. Marshal Raylan Givens as he enforces the law in his hometown of Harlan, Kentucky. The show combines classic Western tropes with modern crime drama. Directed by Graham Yost, starring Timothy Olyphant, Walton Goggins, and Joelle Carter. Produced by FX. It was critically acclaimed.",
        ["Crime", "Western"]
    ],
    "The Leftovers": [
        "A haunting and philosophical drama about life after a mysterious global event.",
        "The Leftovers is set in a world where 2% of the population mysteriously disappears. The show follows the people left behind as they grapple with the inexplicable event and its impact on their lives. Directed by Damon Lindelof and Tom Perrotta, starring Justin Theroux, Carrie Coon, and Amy Brenneman. Produced by HBO. It was critically acclaimed.",
        ["Drama", "Mystery"]
    ],
    "Ted Lasso": [
        "A heartwarming and feel-good sports comedy about an American football coach managing a British soccer team.",
        "Ted Lasso follows an optimistic and unconventional American football coach as he becomes the head coach of a struggling British soccer team. The show is known for its uplifting tone and positive messages. Directed by Bill Lawrence, starring Jason Sudeikis, Hannah Waddingham, and Brett Goldstein. Produced by Apple TV+. It was critically acclaimed.",
        ["Comedy", "Sports"]
    ],
    "Silicon Valley": [
        "A hilarious satire about the cutthroat world of tech startups in Silicon Valley.",
        "Silicon Valley follows a group of software engineers as they try to build a successful tech startup while navigating the absurdities of the tech industry. The show is known for its sharp wit and insightful industry satire. Directed by Mike Judge, starring Thomas Middleditch, T.J. Miller, and Kumail Nanjiani. Produced by HBO. It was critically acclaimed.",
        ["Comedy"]
    ],
    "Mr. Robot": [
        "A gripping and mind-bending thriller about a hacker battling corporate corruption and his own mental health.",
        "Mr. Robot follows Elliot Alderson, a brilliant but troubled hacker, as he becomes involved with a secret organization intent on taking down a corrupt corporation. The show explores themes of technology, mental health, and societal control. Directed by Sam Esmail, starring Rami Malek, Christian Slater, and Carly Chaikin. Produced by USA Network. It was critically acclaimed.",
        ["Thriller", "Drama"]
    ],
    "The IT Crowd": [
        "A quirky British comedy about a group of misfit IT workers.",
        "The IT Crowd is set in the basement of a large corporation and follows the eccentric employees of the IT department as they navigate office life, technical challenges, and absurd situations. Directed by Graham Linehan, starring Chris O'Dowd, Richard Ayoade, and Katherine Parkinson. Produced by Channel 4. It was critically acclaimed.",
        ["Comedy"]
    ],
    "Luther": [
        "A dark and intense crime drama about a brilliant but troubled detective.",
        "Luther follows Detective John Luther, a highly intelligent and dedicated detective who is often consumed by the darkness of the crimes he investigates. The show explores themes of morality, justice, and personal demons. Directed by Neil Cross, starring Idris Elba, Ruth Wilson, and Dermot Crowley. Produced by BBC. It was critically acclaimed.",
        ["Crime", "Drama"]
    ],
    "Killing Eve": [
        "A thrilling and darkly comedic cat-and-mouse game between a spy and an assassin.",
        "Killing Eve follows Eve Polastri, an MI6 agent, and Villanelle, a psychopathic assassin, as they become obsessed with each other in a deadly game of cat and mouse. The show is known for its witty dialogue and complex characters. Directed by Phoebe Waller-Bridge, starring Sandra Oh, Jodie Comer, and Fiona Shaw. Produced by BBC America. It was critically acclaimed.",
        ["Thriller", "Drama"]
    ],
    "Broadchurch": [
        "A gripping crime drama about the investigation of a small-town murder.",
        "Broadchurch follows detectives Alec Hardy and Ellie Miller as they investigate the murder of a young boy in a small coastal town, uncovering secrets and lies within the close-knit community. Directed by Chris Chibnall, starring David Tennant, Olivia Colman, and Jodie Whittaker. Produced by ITV. It was critically acclaimed.",
        ["Crime", "Drama"]
    ],
    "Chilling Adventures of Sabrina": [
        "A dark and supernatural reimagining of the classic character Sabrina the Teenage Witch.",
        "Chilling Adventures of Sabrina follows Sabrina Spellman, a half-witch, half-mortal, as she navigates the challenges of high school and her burgeoning powers, while contending with dark forces in the supernatural world. Directed by Roberto Aguirre-Sacasa, starring Kiernan Shipka, Ross Lynch, and Miranda Otto. Produced by Netflix. It was critically acclaimed.",
        ["Fantasy", "Horror"]
    ],
    "Shadow and Bone": [
        "A fantasy epic based on the Grishaverse novels, following a young woman who discovers she has extraordinary powers.",
        "Shadow and Bone follows Alina Starkov, an orphan and cartographer in a war-torn world, who discovers she has the rare ability to summon light. As she is thrust into the world of the Grisha, she must navigate dark forces and political intrigue. Directed by Eric Heisserer, starring Jessie Mei Li, Ben Barnes, and Archie Renaux. Produced by Netflix. It was critically acclaimed.",
        ["Fantasy", "Drama"]
    ],
    "Shameless (US)": [
        "A dark comedy about a dysfunctional family trying to survive in the South Side of Chicago.",
        "Shameless follows the Gallagher family, led by their alcoholic father Frank, as they struggle to survive in poverty while dealing with chaotic relationships and personal issues. The show is known for its raw portrayal of family dynamics and societal issues. Directed by John Wells, starring William H. Macy, Emmy Rossum, and Jeremy Allen White. Produced by Showtime. It was critically acclaimed.",
        ["Comedy", "Drama"]
    ],
    "The 100": [
        "A post-apocalyptic sci-fi series about survival and leadership as a group of young people return to Earth after a nuclear disaster.",
        "The 100 is set 97 years after a nuclear apocalypse has wiped out almost all life on Earth. A group of 100 juvenile delinquents is sent back to Earth from a space station to see if the planet is habitable again. Directed by Jason Rothenberg, starring Eliza Taylor, Bob Morley, and Marie Avgeropoulos. Produced by The CW. It was critically acclaimed.",
        ["Sci-Fi", "Drama"]
    ],
    "The Punisher": [
        "A gritty superhero series about a man seeking revenge after his family is murdered.",
        "The Punisher follows Frank Castle, a vigilante who seeks to avenge the deaths of his family by eliminating criminals in New York City. The show is dark and action-packed, with themes of justice and moral ambiguity. Directed by Steve Lightfoot, starring Jon Bernthal, Ebon Moss-Bachrach, and Ben Barnes. Produced by Netflix. It was critically acclaimed.",
        ["Action", "Drama"]
    ],
    "His Dark Materials": [
        "An ambitious fantasy series about parallel worlds and a young girl’s quest to uncover hidden truths.",
        "His Dark Materials follows Lyra Belacqua, a young girl from a parallel universe, as she uncovers secrets about a mysterious substance known as Dust. The series is based on the novels by Philip Pullman. Directed by Jack Thorne, starring Dafne Keen, Ruth Wilson, and James McAvoy. Produced by BBC and HBO. It was critically acclaimed.",
        ["Fantasy", "Drama"]
    ],
    "The Umbrella Academy": [
        "A unique superhero series about a dysfunctional family of adopted siblings with extraordinary powers.",
        "The Umbrella Academy follows a group of estranged siblings with special abilities who reunite after the death of their adoptive father to uncover family secrets and prevent an impending apocalypse. Directed by Steve Blackman, starring Ellen Page, Tom Hopper, and David Castañeda. Produced by Netflix. It was critically acclaimed.",
        ["Superhero", "Sci-Fi"]
    ],
    "The End of the F***ing World": [
        "A dark comedy-drama about two misfit teenagers on a road trip that spirals out of control.",
        "The End of the F***ing World follows James, a self-proclaimed psychopath, and Alyssa, a rebellious girl, as they embark on a road trip that leads to unexpected dangers and a growing bond between them. Directed by Jonathan Entwistle, starring Alex Lawther and Jessica Barden. Produced by Netflix. It was critically acclaimed.",
        ["Comedy", "Drama"]
    ],
    "Firefly": [
        "A cult favorite space western about a crew of misfits navigating life on the fringes of a futuristic galaxy.",
        "Firefly is set 500 years in the future and follows the crew of the spaceship Serenity as they take on smuggling jobs and navigate life on the edges of a star system governed by a powerful Alliance. Directed by Joss Whedon, starring Nathan Fillion, Gina Torres, and Alan Tudyk. Produced by Fox. It was critically acclaimed.",
        ["Sci-Fi", "Western"]
    ],
    "Boardwalk Empire": [
        "A sprawling crime drama about political corruption and organized crime during Prohibition in Atlantic City.",
        "Boardwalk Empire chronicles the rise of political boss Enoch 'Nucky' Thompson during Prohibition, blending historical events with fictional characters in a drama about power and crime in Atlantic City. Directed by Terence Winter, starring Steve Buscemi, Kelly Macdonald, and Michael Shannon. Produced by HBO. It was critically acclaimed.",
        ["Crime", "Drama"]
    ],
    "Penny Dreadful": [
        "A gothic horror series that brings together classic literary characters in a chilling narrative.",
        "Penny Dreadful weaves together the stories of iconic characters like Dr. Frankenstein, Dorian Gray, and Dracula, as they confront supernatural threats and personal demons in Victorian London. Directed by John Logan, starring Eva Green, Josh Hartnett, and Timothy Dalton. Produced by Showtime. It was critically acclaimed.",
        ["Horror", "Drama"]
    ],
    "The Blacklist": [
        "A fast-paced crime thriller about an enigmatic criminal helping the FBI catch other dangerous criminals.",
        "The Blacklist follows Raymond 'Red' Reddington, a former criminal mastermind who turns himself in to the FBI and offers to help catch other high-profile criminals under mysterious conditions. Directed by Jon Bokenkamp, starring James Spader, Megan Boone, and Diego Klattenhoff. Produced by NBC. It was critically acclaimed.",
        ["Crime", "Thriller"]
    ],
    "Designated Survivor": [
        "A political thriller about a low-ranking cabinet member who becomes President after an attack on the government.",
        "Designated Survivor follows Tom Kirkman, a low-level cabinet member who suddenly becomes President of the United States after an attack on the Capitol wipes out the government. He must navigate the complexities of politics and national security. Directed by David Guggenheim, starring Kiefer Sutherland, Natascha McElhone, and Adan Canto. Produced by ABC and Netflix. It was critically acclaimed.",
        ["Political Thriller"]
    ],
    "The Morning Show": [
        "A gripping drama about the behind-the-scenes struggles of a morning news show amid scandal.",
        "The Morning Show follows the fallout from a sexual misconduct scandal at a popular morning news show, as the anchors and producers grapple with power dynamics, ethics, and personal ambition. Directed by Mimi Leder, starring Jennifer Aniston, Reese Witherspoon, and Steve Carell. Produced by Apple TV+. It was critically acclaimed.",
        ["Drama"]
    ],
    "Teen Wolf": [
        "A supernatural drama about a high school student who becomes a werewolf and must protect his town from supernatural threats.",
        "Teen Wolf follows Scott McCall, a high school student who is bitten by a werewolf and must deal with his new powers while protecting his town from supernatural creatures and dangers. Directed by Jeff Davis, starring Tyler Posey, Dylan O'Brien, and Holland Roden. Produced by MTV. It was critically acclaimed.",
        ["Fantasy", "Drama"]
    ],
    "Empire": [
        "A dramatic and musical look at the power struggles within a family-owned hip-hop empire.",
        "Empire centers around the Lyon family and their hip-hop entertainment company, as patriarch Lucious Lyon tries to secure a successor while dealing with internal family rivalries and the music industry. Directed by Lee Daniels and Danny Strong, starring Terrence Howard, Taraji P. Henson, and Jussie Smollett. Produced by Fox. It was critically acclaimed.",
        ["Musical", "Drama"]
    ],
    "Gotham": [
        "A dark and gritty origin story for some of DC Comics' most iconic villains and heroes.",
        "Gotham follows a young James Gordon as he rises through the ranks of the Gotham City Police Department, while the origins of villains like Penguin, Riddler, and Joker are explored. Directed by Bruno Heller, starring Ben McKenzie, Donal Logue, and David Mazouz. Produced by Warner Bros. Television. It was critically acclaimed.",
        ["Crime", "Superhero"]
    ],
    "Naruto": [
        "A classic anime series following a young ninja with dreams of becoming the leader of his village.",
        "Naruto follows the journey of Naruto Uzumaki, a young ninja who seeks recognition from his peers and dreams of becoming Hokage, the leader of his village. Along the way, he makes friends and faces powerful enemies. Directed by Hayato Date, starring Junko Takeuchi, Maile Flanagan, and Kate Higgins. Produced by Studio Pierrot. It was critically acclaimed.",
        ["Action", "Adventure", "Anime"]
    ],
    "One Piece": [
        "A long-running anime series about a pirate crew searching for the ultimate treasure.",
        "One Piece follows Monkey D. Luffy and his pirate crew as they search for the legendary treasure known as 'One Piece' in order to become the Pirate King. The series is known for its epic storylines, unique characters, and imaginative world-building. Directed by Konosuke Uda, starring Mayumi Tanaka, Tony Beck, and Laurent Vernin. Produced by Toei Animation. It was critically acclaimed.",
        ["Action", "Adventure", "Anime"]
    ],
    "Goblin Slayer": [
        "A dark fantasy anime about a warrior dedicated to exterminating goblins.",
        "Goblin Slayer follows a warrior known only as the Goblin Slayer, who dedicates his life to hunting and exterminating goblins after they destroyed his village. The series is known for its brutal and gritty approach to fantasy. Directed by Takaharu Ozaki, starring Yuuichirou Umehara, Yui Ogura, and Nao Touyama. Produced by White Fox. It was critically acclaimed.",
        ["Fantasy", "Adventure", "Anime"]
    ],
    "The Seven Deadly Sins": [
        "An action-packed anime about a group of knights on a quest to save their kingdom.",
        "The Seven Deadly Sins follows a group of powerful knights who are framed for plotting to overthrow the kingdom. Together, they must reunite to clear their names and protect the realm from an evil force. Directed by Tensai Okamura, starring Yuki Kaji, Sora Amamiya, and Misaki Kuno. Produced by A-1 Pictures. It was critically acclaimed.",
        ["Action", "Fantasy", "Anime"]
    ],
    "Castlevania": [
        "A dark and gothic anime series about the fight against Dracula and his demonic forces.",
        "Castlevania is set in a medieval world where the last living member of the Belmont clan must fight to save Eastern Europe from the vengeful Dracula, who has unleashed an army of demons upon the world. Directed by Sam Deats, starring Richard Armitage, James Callis, and Alejandra Reynoso. Produced by Netflix. It was critically acclaimed.",
        ["Fantasy", "Action", "Anime"]
    ],
    "Cloudy with a Chance of Meatballs": [
        "A fun and quirky animated film about a scientist who accidentally makes it rain food!",
        "Cloudy with a Chance of Meatballs follows Flint Lockwood, a young inventor who creates a machine that makes food fall from the sky. As the town starts to enjoy the food-based weather, things take a chaotic turn. Directed by Phil Lord and Christopher Miller, starring Bill Hader, Anna Faris, and James Caan. Produced by Sony Pictures Animation. It was critically acclaimed.",
        ["Animation", "Comedy"]
    ],
    "Shrek": [
        "A hilarious and heartwarming fairy tale about an ogre who just wants to be left alone.",
        "Shrek is a reimagining of fairy tales, where an ogre named Shrek embarks on a quest to rescue Princess Fiona to reclaim his swamp from fairytale creatures. Along the way, Shrek learns about friendship and love. Directed by Andrew Adamson and Vicky Jenson, starring Mike Myers, Eddie Murphy, and Cameron Diaz. Produced by DreamWorks Animation. It was critically acclaimed.",
        ["Animation", "Comedy"]
    ],
    "Shrek 2": [
        "A fantastic sequel that brings back Shrek, Fiona, and Donkey in a bigger, funnier adventure!",
        "Shrek 2 follows Shrek and Fiona as they visit her parents in the kingdom of Far Far Away, leading to hilarious misadventures involving a fairy godmother, Prince Charming, and a dashing cat named Puss in Boots. Directed by Andrew Adamson, Kelly Asbury, and Conrad Vernon, starring Mike Myers, Eddie Murphy, and Cameron Diaz. Produced by DreamWorks Animation. It was critically acclaimed.",
        ["Animation", "Comedy"]
    ],
    "The Sandlot": [
        "A nostalgic and heartwarming coming-of-age film about friendship, baseball, and summer fun.",
        "The Sandlot is set in the 1960s and follows a young boy named Scotty Smalls as he moves to a new neighborhood and befriends a group of boys who love baseball. Together, they get into all kinds of mischief, including facing off against a legendary beast. Directed by David Mickey Evans, starring Tom Guiry, Mike Vitar, and Patrick Renna. Produced by 20th Century Fox. It was critically acclaimed.",
        ["Comedy", "Drama", "Family"]
    ],
    "The Shining": [
        "A chilling horror classic about isolation and madness in a haunted hotel.",
        "The Shining follows Jack Torrance, a writer who takes a job as a winter caretaker at the isolated Overlook Hotel, where he slowly descends into madness, putting his wife and son in danger. Directed by Stanley Kubrick, starring Jack Nicholson, Shelley Duvall, and Danny Lloyd. Produced by Warner Bros. It was critically acclaimed.",
        ["Horror", "Thriller"]
    ],
    "Billy Madison": [
        "A silly and outrageous comedy about a grown man going back to school to prove himself.",
        "Billy Madison follows the immature Billy, who must complete grades 1 through 12 in order to inherit his family's fortune and prove to his father that he's ready to take over the family business. Directed by Tamra Davis, starring Adam Sandler, Bradley Whitford, and Bridgette Wilson-Sampras. Produced by Universal Pictures. It was critically acclaimed.",
        ["Comedy"]
    ],
    "Happy Gilmore": [
        "A hilarious sports comedy about a failed hockey player who becomes a professional golfer.",
        "Happy Gilmore follows Happy, a hockey player with anger issues, who discovers a talent for golf and competes in professional tournaments to save his grandmother's house. Directed by Dennis Dugan, starring Adam Sandler, Christopher McDonald, and Julie Bowen. Produced by Universal Pictures. It was critically acclaimed.",
        ["Comedy", "Sports"]
    ],
    "Gladiator": [
        "An epic historical drama about revenge, honor, and survival in the Roman Empire.",
        "Gladiator follows Maximus Decimus Meridius, a betrayed Roman general who becomes a gladiator and seeks vengeance against the corrupt emperor who murdered his family. Directed by Ridley Scott, starring Russell Crowe, Joaquin Phoenix, and Connie Nielsen. Produced by DreamWorks Pictures. It was critically acclaimed.",
        ["Action", "Drama"]
    ],
    "Moulin Rouge!": [
        "A dazzling musical romance set in the bohemian underworld of 19th-century Paris.",
        "Moulin Rouge! tells the story of a young English writer, Christian, who falls in love with Satine, a beautiful courtesan at the Moulin Rouge nightclub, amidst a backdrop of spectacular music and choreography. Directed by Baz Luhrmann, starring Ewan McGregor, Nicole Kidman, and Jim Broadbent. Produced by 20th Century Fox. It was critically acclaimed.",
        ["Musical", "Romance"]
    ],
    "The Lord of the Rings: The Fellowship of the Ring": [
        "An epic fantasy adventure that begins the journey to destroy the One Ring.",
        "The Fellowship of the Ring follows Frodo Baggins, a hobbit who sets out on a quest to destroy the powerful One Ring and prevent the Dark Lord Sauron from taking over Middle-earth. Along the way, he is joined by a diverse group of allies. Directed by Peter Jackson, starring Elijah Wood, Ian McKellen, and Viggo Mortensen. Produced by New Line Cinema. It was critically acclaimed.",
        ["Fantasy", "Adventure"]
    ],
    "Spirited Away": [
        "A stunning and imaginative animated masterpiece about a young girl trapped in a mysterious spirit world.",
        "Spirited Away follows Chihiro, a young girl who stumbles into a magical world and must work at a bathhouse for spirits in order to save her parents. Along the way, she encounters strange creatures and learns valuable life lessons. Directed by Hayao Miyazaki, starring Rumi Hiiragi, Miyu Irino, and Mari Natsuki. Produced by Studio Ghibli. It was critically acclaimed.",
        ["Animation", "Fantasy", "Anime"]
    ],
    "The Dark Knight": [
        "A gritty and intense superhero film featuring one of the most iconic villains of all time.",
        "The Dark Knight continues the story of Batman as he faces off against the chaotic Joker, who threatens Gotham City with a reign of terror. The film explores themes of morality, justice, and sacrifice. Directed by Christopher Nolan, starring Christian Bale, Heath Ledger, and Aaron Eckhart. Produced by Warner Bros. It was critically acclaimed.",
        ["Superhero", "Action"]
    ],
    "A Beautiful Mind": [
        "A moving biographical drama about a brilliant mathematician's struggle with mental illness.",
        "A Beautiful Mind tells the true story of John Nash, a mathematical genius who grapples with schizophrenia while making groundbreaking contributions to economics. Directed by Ron Howard, starring Russell Crowe, Jennifer Connelly, and Ed Harris. Produced by Universal Pictures. It was critically acclaimed.",
        ["Drama", "Biography"]
    ],
    "City of God": [
        "A raw and powerful crime drama set in the slums of Rio de Janeiro.",
        "City of God tells the story of two boys growing up in a violent neighborhood in Rio de Janeiro and how their lives take drastically different paths—one becomes a photographer, and the other a gang leader. Directed by Fernando Meirelles and Kátia Lund, starring Alexandre Rodrigues, Leandro Firmino, and Phellipe Haagensen. Produced by O2 Filmes. It was critically acclaimed.",
        ["Crime", "Drama"]
    ],
    "Finding Nemo": [
        "A heartwarming animated adventure about a father's journey to find his lost son.",
        "Finding Nemo follows Marlin, a clownfish, as he embarks on a perilous journey across the ocean to rescue his son Nemo, who has been captured by a scuba diver. Along the way, he is joined by the forgetful but lovable Dory. Directed by Andrew Stanton, starring Albert Brooks, Ellen DeGeneres, and Alexander Gould. Produced by Pixar Animation Studios. It was critically acclaimed.",
        ["Animation", "Adventure", "Family"]
    ],
    "Eternal Sunshine of the Spotless Mind": [
        "A beautifully unique and emotional film about love, memory, and heartbreak.",
        "Eternal Sunshine of the Spotless Mind follows Joel and Clementine, a couple who undergo a procedure to erase each other from their memories after a painful breakup. The film explores themes of love, regret, and the human desire to forget pain. Directed by Michel Gondry, starring Jim Carrey, Kate Winslet, and Tom Wilkinson. Produced by Focus Features. It was critically acclaimed.",
        ["Sci-Fi", "Romance", "Drama"]
    ],
    "The Incredibles": [
        "A thrilling and funny animated superhero film about a family of undercover heroes.",
        "The Incredibles follows a family of superheroes living undercover in a suburban world that has banned their kind. When a new villain threatens the world, they must return to action to save the day. Directed by Brad Bird, starring Craig T. Nelson, Holly Hunter, and Samuel L. Jackson. Produced by Pixar Animation Studios. It was critically acclaimed.",
        ["Animation", "Action", "Superhero"]
    ],
    "Harry Potter and the Sorcerer's Stone": [
        "The magical beginning of a beloved fantasy series about a boy wizard.",
        "Harry Potter and the Sorcerer's Stone follows young Harry Potter as he discovers he's a wizard and begins his magical education at Hogwarts School of Witchcraft and Wizardry. He soon uncovers a plot involving a dark wizard. Directed by Chris Columbus, starring Daniel Radcliffe, Emma Watson, and Rupert Grint. Produced by Warner Bros. It was critically acclaimed.",
        ["Fantasy", "Adventure"]
    ],
    "The Departed": [
        "A gripping crime thriller about undercover cops and criminals in Boston.",
        "The Departed follows a tense game of cat-and-mouse between an undercover cop infiltrating a mob organization and a mole planted in the police force by the same mob. Directed by Martin Scorsese, starring Leonardo DiCaprio, Matt Damon, and Jack Nicholson. Produced by Warner Bros. It was critically acclaimed.",
        ["Crime", "Thriller"]
    ],
    "No Country for Old Men": [
        "A haunting crime drama about fate, violence, and the consequences of decisions.",
        "No Country for Old Men follows Llewelyn Moss, who stumbles upon drug money and a deadly pursuit ensues, involving a terrifying hitman and an aging sheriff. Directed by Joel and Ethan Coen, starring Josh Brolin, Javier Bardem, and Tommy Lee Jones. Produced by Miramax. It was critically acclaimed.",
        ["Crime", "Drama"]
    ],
    "Slumdog Millionaire": [
        "An inspiring and thrilling tale about destiny, love, and survival.",
        "Slumdog Millionaire tells the story of Jamal, a young man from the slums of Mumbai, who competes on the Indian version of 'Who Wants to Be a Millionaire?' while reflecting on his difficult past. Directed by Danny Boyle, starring Dev Patel, Freida Pinto, and Anil Kapoor. Produced by Fox Searchlight Pictures. It was critically acclaimed.",
        ["Drama", "Romance"]
    ],
    "The Social Network": [
        "A fast-paced drama about the founding of Facebook and the fallout that ensued.",
        "The Social Network chronicles the creation of Facebook by Mark Zuckerberg and the resulting legal battles over the ownership of the company. Directed by David Fincher, starring Jesse Eisenberg, Andrew Garfield, and Justin Timberlake. Produced by Columbia Pictures. It was critically acclaimed.",
        ["Drama", "Biography"]
    ],
    "Brokeback Mountain": [
        "A powerful and emotional love story set against the backdrop of the American West.",
        "Brokeback Mountain follows two cowboys, Ennis and Jack, who form an intimate relationship over several decades despite the societal pressures against them. Directed by Ang Lee, starring Heath Ledger, Jake Gyllenhaal, and Michelle Williams. Produced by Focus Features. It was critically acclaimed.",
        ["Romance", "Drama"]
    ],
    "Pirates of the Caribbean: The Curse of the Black Pearl": [
        "A swashbuckling adventure about pirates, curses, and buried treasure.",
        "Pirates of the Caribbean follows Captain Jack Sparrow as he teams up with blacksmith Will Turner to save Elizabeth Swann from cursed pirates aboard the Black Pearl. Directed by Gore Verbinski, starring Johnny Depp, Orlando Bloom, and Keira Knightley. Produced by Walt Disney Pictures. It was critically acclaimed.",
        ["Action", "Adventure"]
    ],
    "The Aviator": [
        "An ambitious biographical drama about the life of Howard Hughes, an eccentric aviation pioneer.",
        "The Aviator follows the life of Howard Hughes, covering his achievements in aviation, filmmaking, and his descent into obsessive-compulsive disorder. Directed by Martin Scorsese, starring Leonardo DiCaprio, Cate Blanchett, and Kate Beckinsale. Produced by Miramax. It was critically acclaimed.",
        ["Drama", "Biography"]
    ],
    "The Pursuit of Happyness": [
        "An inspiring story of perseverance and the American Dream, based on a true story.",
        "The Pursuit of Happyness follows Chris Gardner, a struggling salesman who becomes homeless but never gives up on his dream of providing a better life for his son, eventually becoming a successful stockbroker. Directed by Gabriele Muccino, starring Will Smith, Jaden Smith, and Thandie Newton. Produced by Columbia Pictures. It was critically acclaimed.",
        ["Drama", "Biography"]
    ],
    "Avatar": [
        "A visually stunning and immersive sci-fi film about colonization and resistance on a distant planet.",
        "Avatar follows Jake Sully, a paraplegic former Marine, who is sent to the alien planet Pandora to gather intelligence on the Na'vi people. He becomes torn between his human mission and his growing bond with the Na'vi. Directed by James Cameron, starring Sam Worthington, Zoe Saldana, and Sigourney Weaver. Produced by 20th Century Fox. It was critically acclaimed.",
        ["Sci-Fi", "Adventure"]
    ],
    "The Queen": [
        "A fascinating drama about the British royal family’s reaction to Princess Diana's death.",
        "The Queen examines the tense relationship between Queen Elizabeth II and Prime Minister Tony Blair in the aftermath of Princess Diana's death, as the nation mourns and the monarchy faces scrutiny. Directed by Stephen Frears, starring Helen Mirren, Michael Sheen, and James Cromwell. Produced by Pathé. It was critically acclaimed.",
        ["Drama", "Biography"]
    ],
    "Tropic Thunder": [
        "A wild and outrageous action-comedy about a group of actors filming a war movie who get caught in real danger.",
        "Tropic Thunder follows a group of actors who, while filming a Vietnam War movie, unwittingly find themselves in an actual conflict. The film is filled with sharp satire and memorable characters. Directed by Ben Stiller, starring Ben Stiller, Robert Downey Jr., and Jack Black. Produced by DreamWorks Pictures. It was critically acclaimed.",
        ["Comedy", "Action"]
    ],
    "Little Miss Sunshine": [
        "A heartwarming and funny road trip comedy about a dysfunctional family.",
        "Little Miss Sunshine follows the Hoover family as they take a road trip in their van to support their daughter Olive in a children's beauty pageant. Along the way, they confront their personal struggles and bond as a family. Directed by Jonathan Dayton and Valerie Faris, starring Steve Carell, Toni Collette, and Abigail Breslin. Produced by Fox Searchlight Pictures. It was critically acclaimed.",
        ["Comedy", "Drama"]
    ],
    "Crouching Tiger, Hidden Dragon": [
        "A visually stunning martial arts epic about love, honor, and destiny.",
        "Crouching Tiger, Hidden Dragon tells the story of two warriors in pursuit of a stolen sword and the young noblewoman at the center of the conflict. The film is known for its breathtaking fight choreography. Directed by Ang Lee, starring Chow Yun-fat, Michelle Yeoh, and Zhang Ziyi. Produced by Sony Pictures Classics. It was critically acclaimed.",
        ["Action", "Adventure"]
    ],
    "Lost in Translation": [
        "A touching and introspective drama about loneliness and human connection.",
        "Lost in Translation follows Bob Harris, an aging actor, and Charlotte, a young woman, as they form an unlikely bond while staying in a Tokyo hotel, navigating personal and cultural isolation. Directed by Sofia Coppola, starring Bill Murray, Scarlett Johansson, and Giovanni Ribisi. Produced by Focus Features. It was critically acclaimed.",
        ["Drama", "Romance"]
    ],
    "V for Vendetta": [
        "A bold and stylish dystopian thriller about resistance against tyranny.",
        "V for Vendetta is set in a future totalitarian Britain, where a masked vigilante known only as V works to ignite revolution against a corrupt government. Directed by James McTeigue, starring Natalie Portman, Hugo Weaving, and Stephen Rea. Produced by Warner Bros. It was critically acclaimed.",
        ["Action", "Thriller"]
    ],
    "The 40-Year-Old Virgin": [
        "A hilarious and heartfelt comedy about a man trying to lose his virginity at 40.",
        "The 40-Year-Old Virgin follows Andy Stitzer, a middle-aged man who has never had sex, as his well-meaning friends try to help him overcome his shyness and meet women. Directed by Judd Apatow, starring Steve Carell, Paul Rudd, and Seth Rogen. Produced by Universal Pictures. It was critically acclaimed.",
        ["Comedy", "Romance"]
    ],
    "Bridesmaids": [
        "A hilarious and relatable comedy about friendship and the chaos of wedding planning.",
        "Bridesmaids follows Annie, a down-on-her-luck woman who becomes the maid of honor for her best friend's wedding, leading to a series of chaotic and hilarious events. Directed by Paul Feig, starring Kristen Wiig, Maya Rudolph, and Melissa McCarthy. Produced by Universal Pictures. It was critically acclaimed.",
        ["Comedy", "Romance"]
    ],
    "The Hangover": [
        "A hilarious and outrageous comedy about a bachelor party gone wrong in Las Vegas.",
        "The Hangover follows a group of friends who travel to Las Vegas for a bachelor party. After a wild night of partying, they wake up with no memory of what happened and must retrace their steps to find the missing groom. Directed by Todd Phillips, starring Bradley Cooper, Ed Helms, and Zach Galifianakis. Produced by Warner Bros. It was critically acclaimed.",
        ["Comedy"]
    ],
    "Zodiac": [
        "A chilling crime thriller about the search for the infamous Zodiac killer.",
        "Zodiac is based on the true story of the police and journalists who hunted the Zodiac killer, a serial murderer who terrorized the San Francisco Bay Area in the late 1960s. Directed by David Fincher, starring Jake Gyllenhaal, Robert Downey Jr., and Mark Ruffalo. Produced by Paramount Pictures. It was critically acclaimed.",
        ["Crime", "Thriller"]
    ],
    "Inside Out": [
        "A heartwarming and imaginative animated film about the emotions inside a young girl’s mind.",
        "Inside Out follows Riley, an 11-year-old girl, and her emotions—Joy, Sadness, Anger, Fear, and Disgust—who must work together when Riley's family moves to a new city. Directed by Pete Docter, starring Amy Poehler, Phyllis Smith, and Bill Hader. Produced by Pixar Animation Studios. It was critically acclaimed.",
        ["Animation", "Comedy", "Family"]
    ],
    "The Shape of Water": [
        "A hauntingly beautiful romance between a mute woman and a mysterious sea creature.",
        "The Shape of Water follows Elisa, a mute woman working in a government lab during the Cold War, who forms a bond with an amphibious creature being held in captivity. Directed by Guillermo del Toro, starring Sally Hawkins, Michael Shannon, and Octavia Spencer. Produced by Fox Searchlight Pictures. It was critically acclaimed.",
        ["Fantasy", "Romance", "Drama"]
    ],
    "12 Years a Slave": [
        "A powerful and emotional historical drama about a free man sold into slavery.",
        "12 Years a Slave is based on the true story of Solomon Northup, a free African-American man who is kidnapped and sold into slavery in the 1840s. He fights to regain his freedom against all odds. Directed by Steve McQueen, starring Chiwetel Ejiofor, Michael Fassbender, and Lupita Nyong'o. Produced by Regency Enterprises. It was critically acclaimed.",
        ["Historical", "Drama"]
    ],
    "The Grand Budapest Hotel": [
        "A quirky and visually stunning comedy-drama set in a luxury hotel in the 1930s.",
        "The Grand Budapest Hotel follows the adventures of Gustave H., a legendary concierge, and his protégé Zero, as they become embroiled in a murder mystery and the theft of a priceless painting. Directed by Wes Anderson, starring Ralph Fiennes, Tony Revolori, and Saoirse Ronan. Produced by Fox Searchlight Pictures. It was critically acclaimed.",
        ["Comedy", "Drama"]
    ],
    "Get Out": [
        "A brilliantly crafted horror-thriller that explores race, paranoia, and identity.",
        "Get Out follows Chris, a young African-American man who uncovers shocking secrets when he visits the family of his white girlfriend for the first time. The film blends horror with social commentary. Directed by Jordan Peele, starring Daniel Kaluuya, Allison Williams, and Bradley Whitford. Produced by Universal Pictures. It was critically acclaimed.",
        ["Horror", "Thriller"]
    ],
    "Django Unchained": [
        "A thrilling and violent western about a freed slave seeking revenge and justice.",
        "Django Unchained follows Django, a former slave, who teams up with a bounty hunter to rescue his wife from a brutal plantation owner in the Antebellum South. Directed by Quentin Tarantino, starring Jamie Foxx, Christoph Waltz, and Leonardo DiCaprio. Produced by The Weinstein Company. It was critically acclaimed.",
        ["Western", "Action"]
    ],
    "Silver Linings Playbook": [
        "A heartwarming and offbeat romantic comedy about two people rebuilding their lives after personal setbacks.",
        "Silver Linings Playbook follows Pat, a man with bipolar disorder, who forms an unexpected bond with Tiffany, a young widow dealing with her own struggles. Together, they find healing and hope. Directed by David O. Russell, starring Bradley Cooper, Jennifer Lawrence, and Robert De Niro. Produced by The Weinstein Company. It was critically acclaimed.",
        ["Romance", "Comedy"]
    ],
    "The Help": [
        "A powerful drama about race, friendship, and social change in 1960s Mississippi.",
        "The Help is set during the Civil Rights Movement and follows three women—a young white writer and two African-American maids—who form an unlikely friendship while documenting the untold stories of black maids working for white families. Directed by Tate Taylor, starring Viola Davis, Octavia Spencer, and Emma Stone. Produced by DreamWorks Pictures. It was critically acclaimed.",
        ["Drama"]
    ],
    "Black Swan": [
        "A dark and psychological thriller about the pressures of perfection in the world of ballet.",
        "Black Swan follows Nina, a ballerina who begins to unravel as she competes for the lead role in 'Swan Lake.' The film explores themes of obsession, control, and identity. Directed by Darren Aronofsky, starring Natalie Portman, Mila Kunis, and Vincent Cassel. Produced by Fox Searchlight Pictures. It was critically acclaimed.",
        ["Thriller", "Drama"]
    ],
    "Moonlight": [
        "A deeply moving and intimate coming-of-age story about a young African-American man growing up in a rough Miami neighborhood.",
        "Moonlight is told in three parts, following Chiron as he navigates the complexities of identity, sexuality, and the challenges of growing up in a hostile environment. Directed by Barry Jenkins, starring Mahershala Ali, Naomie Harris, and Trevante Rhodes. Produced by A24. It was critically acclaimed.",
        ["Drama"]
    ],
    "Spotlight": [
        "An investigative drama about the Boston Globe's Pulitzer Prize-winning exposé of child abuse in the Catholic Church.",
        "Spotlight follows a team of journalists as they uncover a decades-long cover-up of child abuse by Catholic priests in Boston. Directed by Tom McCarthy, starring Mark Ruffalo, Michael Keaton, and Rachel McAdams. Produced by Open Road Films. It was critically acclaimed.",
        ["Drama", "Biography"]
    ],
    "Mad Max: Fury Road": [
        "A high-octane action film set in a post-apocalyptic wasteland where survival is key.",
        "Mad Max: Fury Road follows Max Rockatansky as he teams up with Imperator Furiosa to escape a tyrant and free enslaved women in a wild chase across the desert. Directed by George Miller, starring Tom Hardy, Charlize Theron, and Nicholas Hoult. Produced by Warner Bros. It was critically acclaimed.",
        ["Action", "Sci-Fi"]
    ],
    "The Big Short": [
        "A sharp and funny drama about the 2008 financial crisis and the people who saw it coming.",
        "The Big Short follows a group of investors who bet against the housing market before the 2008 financial collapse, exposing the greed and corruption within the banking system. Directed by Adam McKay, starring Christian Bale, Steve Carell, and Ryan Gosling. Produced by Paramount Pictures. It was critically acclaimed.",
        ["Comedy", "Drama"]
    ],
    "Birdman": [
        "A visually unique and darkly comic film about a washed-up actor trying to regain his former glory.",
        "Birdman follows Riggan Thomson, a former movie star famous for playing a superhero, as he struggles to mount a Broadway comeback while grappling with his personal and professional crises. Directed by Alejandro González Iñárritu, starring Michael Keaton, Edward Norton, and Emma Stone. Produced by Fox Searchlight Pictures. It was critically acclaimed.",
        ["Comedy", "Drama"]
    ],
    "The Revenant": [
        "A visceral survival drama about a frontiersman seeking revenge after being left for dead.",
        "The Revenant follows Hugh Glass, a frontiersman who is left for dead after being mauled by a bear. He embarks on a harrowing journey through the wilderness to exact revenge on those who betrayed him. Directed by Alejandro González Iñárritu, starring Leonardo DiCaprio, Tom Hardy, and Domhnall Gleeson. Produced by 20th Century Fox. It was critically acclaimed.",
        ["Drama", "Adventure"]
    ],
    "Gravity": [
        "A visually breathtaking space thriller about survival and isolation.",
        "Gravity follows two astronauts who are stranded in space after a devastating accident and must work together to survive and return to Earth. Directed by Alfonso Cuarón, starring Sandra Bullock and George Clooney. Produced by Warner Bros. It was critically acclaimed.",
        ["Sci-Fi", "Thriller"]
    ],
    "Her": [
        "A deeply emotional and thought-provoking sci-fi romance about a man falling in love with an AI.",
        "Her follows Theodore, a lonely writer who develops a relationship with an AI operating system named Samantha. The film explores themes of love, technology, and human connection. Directed by Spike Jonze, starring Joaquin Phoenix, Scarlett Johansson, and Amy Adams. Produced by Annapurna Pictures. It was critically acclaimed.",
        ["Sci-Fi", "Romance"]
    ],
    "Interstellar": [
        "A visually stunning and mind-bending sci-fi epic about humanity's survival and exploration of the cosmos.",
        "Interstellar follows a group of astronauts who travel through a wormhole in search of a new home for humanity as Earth becomes uninhabitable. Directed by Christopher Nolan, starring Matthew McConaughey, Anne Hathaway, and Jessica Chastain. Produced by Paramount Pictures. It was critically acclaimed.",
        ["Sci-Fi", "Drama"]
    ],
    "Wonder Woman": [
        "An inspiring and action-packed superhero origin story about the Amazon warrior Diana.",
        "Wonder Woman follows Diana, an Amazon princess, as she leaves her island home to help end World War I and discovers her full powers as Wonder Woman. Directed by Patty Jenkins, starring Gal Gadot, Chris Pine, and Connie Nielsen. Produced by Warner Bros. It was critically acclaimed.",
        ["Superhero", "Action"]
    ],
    "La La Land": [
        "A beautifully crafted musical romance about following your dreams in Los Angeles.",
        "La La Land follows aspiring actress Mia and jazz musician Sebastian as they fall in love while pursuing their artistic dreams in a city known for heartbreak and success. Directed by Damien Chazelle, starring Ryan Gosling and Emma Stone. Produced by Lionsgate. It was critically acclaimed.",
        ["Musical", "Romance"]
    ],
    "Whiplash": [
        "An intense and gripping drama about a young drummer’s pursuit of greatness.",
        "Whiplash follows Andrew, a talented young drummer, who enrolls at a prestigious music conservatory and becomes the pupil of a ruthless, perfectionist instructor. The film explores themes of ambition, sacrifice, and abuse. Directed by Damien Chazelle, starring Miles Teller, J.K. Simmons, and Paul Reiser. Produced by Bold Films. It was critically acclaimed.",
        ["Drama", "Music"]
    ],
    "Parasite": [
        "A thrilling and darkly comedic film about class, deception, and survival.",
        "Parasite follows the impoverished Kim family as they con their way into the lives of a wealthy family, leading to unexpected consequences. The film explores the growing divide between the rich and the poor. Directed by Bong Joon Ho, starring Song Kang-ho, Lee Sun-kyun, and Cho Yeo-jeong. Produced by CJ Entertainment. It was critically acclaimed.",
        ["Thriller", "Drama"]
    ],
    "The Big Lebowski": [
        "A cult classic comedy about an easy-going man caught in a bizarre crime scheme.",
        "The Big Lebowski follows Jeffrey 'The Dude' Lebowski, a laid-back slacker who is mistaken for a millionaire and gets drawn into a series of misadventures involving ransom and bowling. Directed by Joel Coen, starring Jeff Bridges, John Goodman, and Julianne Moore. Produced by PolyGram Filmed Entertainment. It was critically acclaimed.",
        ["Comedy", "Crime"]
    ],
    "The Wolf of Wall Street": [
        "A wild and outrageous biographical drama about greed, excess, and financial corruption.",
        "The Wolf of Wall Street chronicles the rise and fall of stockbroker Jordan Belfort, who made a fortune through fraud and corruption on Wall Street, only to be brought down by the FBI. Directed by Martin Scorsese, starring Leonardo DiCaprio, Jonah Hill, and Margot Robbie. Produced by Paramount Pictures. It was critically acclaimed.",
        ["Comedy", "Drama"]
    ],
    "Black Panther": [
        "An epic superhero film that celebrates African culture and identity.",
        "Black Panther follows T'Challa as he returns to his technologically advanced African nation of Wakanda to claim the throne, only to face challenges from a powerful adversary. Directed by Ryan Coogler, starring Chadwick Boseman, Michael B. Jordan, and Lupita Nyong'o. Produced by Marvel Studios. It was critically acclaimed.",
        ["Superhero", "Action"]
    ],
    "The Sixth Sense": [
        "A chilling supernatural thriller with one of the most iconic plot twists in cinema history.",
        "The Sixth Sense follows a troubled young boy who claims to see ghosts, and the psychologist who tries to help him, leading to a shocking discovery. Directed by M. Night Shyamalan, starring Bruce Willis, Haley Joel Osment, and Toni Collette. Produced by Hollywood Pictures. It was critically acclaimed.",
        ["Thriller", "Mystery"]
    ],
    "Guardians of the Galaxy": [
        "A fun and action-packed space adventure about a ragtag group of heroes saving the galaxy.",
        "Guardians of the Galaxy follows a group of misfits, including Star-Lord, Gamora, Drax, Rocket, and Groot, who must work together to stop a villain from destroying the galaxy. Directed by James Gunn, starring Chris Pratt, Zoe Saldana, and Dave Bautista. Produced by Marvel Studios. It was critically acclaimed.",
        ["Superhero", "Sci-Fi"]
    ],
    "The Usual Suspects": [
        "A brilliant crime thriller with an unforgettable twist ending.",
        "The Usual Suspects follows five criminals who are brought together by a mysterious figure known as Keyser Söze, leading to a complex web of deception, betrayal, and murder. Directed by Bryan Singer, starring Kevin Spacey, Gabriel Byrne, and Chazz Palminteri. Produced by PolyGram Filmed Entertainment. It was critically acclaimed.",
        ["Crime", "Thriller"]
    ],
    "Deadpool": [
        "A hilarious and irreverent superhero film that breaks all the rules.",
        "Deadpool follows Wade Wilson, a former special forces operative who becomes the wisecracking antihero Deadpool after a rogue experiment gives him accelerated healing powers. Directed by Tim Miller, starring Ryan Reynolds, Morena Baccarin, and Ed Skrein. Produced by 20th Century Fox. It was critically acclaimed.",
        ["Superhero", "Comedy"]
    ],
    "Joker": [
        "A dark and gritty character study about a man’s descent into madness and violence.",
        "Joker explores the origins of the iconic DC villain, focusing on Arthur Fleck, a failed comedian who turns to crime and chaos as he loses his grip on reality. Directed by Todd Phillips, starring Joaquin Phoenix, Robert De Niro, and Zazie Beetz. Produced by Warner Bros. It was critically acclaimed.",
        ["Thriller", "Drama"]
    ],
    "Blade Runner 2049": [
        "A visually stunning sci-fi sequel that explores identity, humanity, and the future.",
        "Blade Runner 2049 follows K, a replicant blade runner, as he uncovers a secret that could destabilize society and embarks on a journey to find former blade runner Rick Deckard. Directed by Denis Villeneuve, starring Ryan Gosling, Harrison Ford, and Ana de Armas. Produced by Warner Bros. It was critically acclaimed.",
        ["Sci-Fi", "Thriller"]
    ],
    "Spider-Man: Into the Spider-Verse": [
        "A groundbreaking animated superhero film that introduces multiple versions of Spider-Man.",
        "Spider-Man: Into the Spider-Verse follows Miles Morales, a teenager who becomes Spider-Man after gaining superpowers, and joins forces with different versions of Spider-Man from other dimensions to stop a threat to the multiverse. Directed by Peter Ramsey, Rodney Rothman, and Bob Persichetti, starring Shameik Moore, Jake Johnson, and Hailee Steinfeld. Produced by Sony Pictures Animation. It was critically acclaimed.",
        ["Animation", "Superhero"]
    ],
    "Logan": [
        "A gritty and emotional superhero film that marks the end of Wolverine’s journey.",
        "Logan follows an aging Wolverine as he cares for a frail Professor X while protecting a young mutant girl from dangerous forces. The film blends superhero action with a poignant narrative about loss and redemption. Directed by James Mangold, starring Hugh Jackman, Patrick Stewart, and Dafne Keen. Produced by 20th Century Fox. It was critically acclaimed.",
        ["Superhero", "Drama"]
    ],
    "Birdman": [
        "A visually unique and darkly comic film about a washed-up actor trying to regain his former glory.",
        "Birdman follows Riggan Thomson, a former movie star famous for playing a superhero, as he struggles to mount a Broadway comeback while grappling with his personal and professional crises. Directed by Alejandro González Iñárritu, starring Michael Keaton, Edward Norton, and Emma Stone. Produced by Fox Searchlight Pictures. It was critically acclaimed.",
        ["Comedy", "Drama"]
    ],
    "12 Years a Slave": [
        "A powerful and emotional historical drama about a free man sold into slavery.",
        "12 Years a Slave is based on the true story of Solomon Northup, a free African-American man who is kidnapped and sold into slavery in the 1840s. He fights to regain his freedom against all odds. Directed by Steve McQueen, starring Chiwetel Ejiofor, Michael Fassbender, and Lupita Nyong'o. Produced by Regency Enterprises. It was critically acclaimed.",
        ["Historical", "Drama"]
    ],
    "The Intouchables": [
        "A heartwarming French comedy-drama about an unlikely friendship between a wealthy man and his caregiver.",
        "The Intouchables follows Philippe, a quadriplegic aristocrat, who hires Driss, a lively young man from the projects, to be his caregiver. The film explores their growing friendship and the ways they enrich each other's lives. Directed by Olivier Nakache and Éric Toledano, starring François Cluzet and Omar Sy. Produced by Gaumont. It was critically acclaimed.",
        ["Comedy", "Drama"]
    ],
    "Amélie": [
        "A whimsical and charming French romance about a shy woman who changes the lives of those around her.",
        "Amélie follows a young woman with a vivid imagination who decides to help others find happiness while discovering love for herself in the process. Directed by Jean-Pierre Jeunet, starring Audrey Tautou, Mathieu Kassovitz, and Rufus. Produced by Canal+. It was critically acclaimed.",
        ["Romance", "Comedy"]
    ],
    "Requiem for a Dream": [
        "A haunting and visually striking drama about addiction and the human condition.",
        "Requiem for a Dream explores the lives of four individuals whose dreams and ambitions are destroyed by their addictions, leading them down a path of self-destruction. Directed by Darren Aronofsky, starring Jared Leto, Jennifer Connelly, and Ellen Burstyn. Produced by Artisan Entertainment. It was critically acclaimed.",
        ["Drama"]
    ],
    "The Prestige": [
        "A thrilling and mysterious drama about two rival magicians caught in a deadly competition.",
        "The Prestige follows Robert Angier and Alfred Borden, two magicians in 19th-century London, whose rivalry drives them to make dangerous sacrifices in the pursuit of the ultimate illusion. Directed by Christopher Nolan, starring Hugh Jackman, Christian Bale, and Scarlett Johansson. Produced by Warner Bros. It was critically acclaimed.",
        ["Mystery", "Sci-Fi"]
    ],
    "Oldboy": [
        "A twisted and violent revenge thriller with a shocking conclusion.",
        "Oldboy follows a man who is mysteriously imprisoned for 15 years and then released, with no explanation, as he seeks revenge against his captors while unraveling the mystery of his confinement. Directed by Park Chan-wook, starring Choi Min-sik, Yoo Ji-tae, and Kang Hye-jung. Produced by Show East. It was critically acclaimed.",
        ["Thriller", "Mystery"]
    ],
    "Mulholland Drive": [
        "A surreal and enigmatic thriller about Hollywood, dreams, and identity.",
        "Mulholland Drive follows an aspiring actress who arrives in Los Angeles and becomes entangled in a complex mystery involving a car accident, a woman with amnesia, and strange visions. Directed by David Lynch, starring Naomi Watts, Laura Harring, and Justin Theroux. Produced by Universal Pictures. It was critically acclaimed.",
        ["Mystery", "Drama"]
    ],
    "Zodiac": [
        "A chilling crime thriller about the search for the infamous Zodiac killer.",
        "Zodiac is based on the true story of the police and journalists who hunted the Zodiac killer, a serial murderer who terrorized the San Francisco Bay Area in the late 1960s. Directed by David Fincher, starring Jake Gyllenhaal, Robert Downey Jr., and Mark Ruffalo. Produced by Paramount Pictures. It was critically acclaimed.",
        ["Crime", "Thriller"]
    ],
    "Pan's Labyrinth": [
        "A dark and visually stunning fantasy about a young girl’s journey through a magical labyrinth.",
        "Pan's Labyrinth follows Ofelia, a young girl in post-Civil War Spain, as she escapes into a dark and twisted fantasy world filled with mythical creatures, while her real world becomes increasingly violent. Directed by Guillermo del Toro, starring Ivana Baquero, Sergi López, and Maribel Verdú. Produced by Warner Bros. It was critically acclaimed.",
        ["Fantasy", "War"]
    ]
}