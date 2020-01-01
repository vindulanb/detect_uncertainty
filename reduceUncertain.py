# Used by stemmer
# import nltk.corpus
# from nltk.stem import PorterStemmer

from nltk.tokenize import word_tokenize
from Detect_uncertain.interpreter_functions import *

def find_uncertain_meaning(raw_text_input):
    object_caption = ""
    distance_to_object = ""
    text_input = ""
    slpitter = ","

    # Split and set variables
    try:
        data_list = raw_text_input.split(slpitter)
        text_input = data_list[0]
        object_caption = data_list[1]
        distance_to_object = float(data_list[2])
    except:
        print("splitter error!")

    splitAndSet(raw_text_input, ',')
    # print(object_caption + "/" + distance_to_object + "/" + text_input + "/")
    # TODO comment this after use demo
    text_input = "quickly go near the staircase"
    print("\nInput : " + text_input + "\n")

    # Convert into lowercase
    text_input = text_input.lower()

    # Input string tokenization
    words = word_tokenize(text_input)

    # Replace list with stemmed words
    # ps = PorterStemmer()
    # words[:] = [ps.stem(w) for w in words]

    # Initialize the grammar
    chink_grammar = r"""
        UND: #chunk uncertain distance
        {<VB|VBP><TO|DT>?(<NN|RB|RBR|RBS|JJ|JJR|JJS|IN|NNS>){1,2}} #chunk regex sequence
        }<WP|WDT>+{ #chink complement
        
        OBJ: #chunk Object
        {<IN|TO|DT>{0,2}<NN|JJ>} #chunk regex sequence
        }<WP|WDT>+{ #chink complement
        
        UNV: #chunk uncertain velocity
        {<NN|JJ|JJR|JJS|RB|RBR|RBS>{0,3}} #chunk regex sequence
        }<WP|WDT>+{ #chink complement
        """

    # Adding pos tags to the sentence
    input_pos_tokens = nltk.pos_tag(words)

    # Check input format fulfill the grammar
    chink_parser = nltk.RegexpParser(chink_grammar)

    # Denote result tree of categorized words
    try:
        result_tree = chink_parser.parse(input_pos_tokens)
    except:
        print("An exception occurred")
        result_tree = 0

    text_input_tokens_without_pos = words
    print("\nTokens with POS tags:")

    # Representation of words  with adding POS tags
    for token in text_input_tokens_without_pos:
        print(nltk.pos_tag([token]))

    print(input_pos_tokens)

    # Calling a function to filter the chunks having uncertain distance
    distance_part = filterChunk(result_tree, 'UND')
    print("\nFiltered output command part:")
    print(distance_part)

    # Calling a function to filter the chunks having pointed object
    object_part = filterChunk(result_tree, 'OBJ')
    print("\nFiltered output object part:")
    print(object_part)

    # Calling a function to filter the chunks having uncertain velocity
    try:
        if filterChunk(result_tree, 'UNV'):
            velocity_part = filterChunk(result_tree, 'UNV')
            print("\nFiltered output velocity part:")
        else:
            velocity_part = "[default]"
    except:
        velocity_part = "[default]"

    print(velocity_part)

    # Adding pos tags to the command_part
    distance_pos_tokens = nltk.pos_tag(word_tokenize(distance_part))

    # Adding pos tags to the object_part
    object_pos_tokens = nltk.pos_tag(word_tokenize(object_part))

    # Adding pos tags to the velocity_part
    velocity_pos_tokens = nltk.pos_tag(word_tokenize(velocity_part))

    # real_world_object = ""
    # uncertain_distance = ""
    # uncertain_velocity = ""

    # Extracting the uncertain distance
    uncertain_distance = getUncertain(distance_pos_tokens)

    # Extracting the uncertain velocity
    uncertain_velocity = getUncertainVelocity(velocity_pos_tokens)
    if uncertain_velocity == "":
        uncertain_velocity = getUncertainVelocity(distance_pos_tokens)

    # Extracting the object
    real_world_object = getObject(object_pos_tokens)

    # Extracted data from input String
    print("\n")
    print("Pointed object : ", real_world_object)

    # is superlative or comparative for distance part
    dis_position = superlativeOrComparative(distance_pos_tokens, velocity_pos_tokens, uncertain_distance)
    print("Uncertain distance : ", uncertain_distance, " >> dis_position(Multiplier >> ", dis_position, ")")

    # is superlative or comparative for velocity part
    velo_position = superlativeOrComparative(distance_pos_tokens, velocity_pos_tokens, uncertain_velocity)
    print("Uncertain velocity : ", uncertain_velocity, " >> velo_position(Multiplier >> ", velo_position, ")")

    # TODO multiplier does not detect very ; there are 2 multipliers for UNV & UND
    # up to @minila
    # Find distance multiplier
    multiplier_word = getMultiplier(words, uncertain_velocity)
    print("Velocity multiplier : ", multiplier_word)

    # Connects to knowledge-expert and find meaning for uncertainty
    jar_path = "java -jar C:/Users/Admin/PycharmProjects/untitled1/ontology/dist/ontology.jar "
    # converts superlative and comparative
    argument = getBaseFormat(uncertain_distance, dis_position)
    uncertain_distance_numeric = javaRun(jar_path, argument)
    if uncertain_distance_numeric == 0:
        webCrawlThis(argument)
    uncertain_distance_numeric = javaRun(jar_path, argument)
    print("\nThe numeric value for word " + argument + ", from Ontology : " + str(uncertain_distance_numeric))

    # Connects to knowledge-expert and find meaning for Multiplier
    jar_path = "java -jar C:/Users/Admin/PycharmProjects/untitled1/ontology/dist/ontology.jar "
    argument = dis_position
    multiplier = javaRun(jar_path, argument)
    print("\nThe numeric value for multiplier " + dis_position + ", from Ontology : " + str(multiplier))

    # Calculate the distance to be travelled
    distance_to_travel = calculateDistanceToTravel(distance_to_object, multiplier, uncertain_distance_numeric)
    print("Distance needed to be traveled : ", distance_to_travel)

    # String information converted into a machine understandable dictionary
    machineReadableData = {
        "distance": 0.0,
        "object": "tree",
        "direction": 120.0,
        "velocity": 7
    }

    # TODO building the information
    # Updating the dictionary value according to the Ontology knowledge base
    machineReadableData["distance"] = 4.5
