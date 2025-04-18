import random as r

# artist,artistIds,asciiName,attractionLights,availability,boosterTypes,borderColor,cardParts,colorIdentity,colorIndicator,colors,defense,duelDeck,edhrecRank,edhrecSaltiness,faceConvertedManaCost,faceFlavorName,faceManaValue,faceName,finishes,flavorName,flavorText,frameEffects,frameVersion,hand,hasAlternativeDeckLimit,hasContentWarning,hasFoil,hasNonFoil,isAlternative,isFullArt,isFunny,isGameChanger,isOnlineOnly,isOversized,isPromo,isRebalanced,isReprint,isReserved,isStarter,isStorySpotlight,isTextless,isTimeshifted,keywords,language,layout,leadershipSkills,life,loyalty,manaCost,manaValue,name,number,originalPrintings,originalReleaseDate,originalText,originalType,otherFaceIds,power,printings,promoTypes,rarity,rebalancedPrintings,relatedCards,securityStamp,setCode,side,signature,sourceProducts,subsets,subtypes,supertypes,text,toughness,type,types,uuid,variations,watermark
# data = "the sun shined on the white road"
with open("Beaver Hacks/Database/AllPrintingsCSVFiles/cards.csv", "r") as test:
    data = test.read()

tokens = list(data.lower().split(","))
# print(len(tokens))

vocab, index = {}, 1  # start indexing from 1
vocab['<pad>'] = 0  # add a padding token
for token in tokens:
    if token not in vocab:
        vocab[token] = index
        index += 1
vocab_size = len(vocab)
# print(vocab_size)
# print(vocab)

inverse_vocab = {index: token for token, index in vocab.items()}
# print(inverse_vocab)

example_sequence = [vocab[word] for word in tokens]
# print(example_sequence)

tupleArray = []
windowSize = 2

for i in range(1, windowSize + 1):
    for key, word in inverse_vocab.items():
        if key > i-1 and key <= len(inverse_vocab)-(i+1):
            word2 = inverse_vocab[key+i]
            tupleArray.append((key, vocab[word2]))
            tupleArray.append((key, inverse_vocab[key+i]))
            if inverse_vocab[key-i] != "<pad>":
                word2 = inverse_vocab[key-i]
                tupleArray.append((key,vocab[word2]))
                tupleArray.append((word, inverse_vocab[key-i]))

dictonary = {}

for i in range(0, len(tupleArray), 2):
    key = tupleArray[i]
    value = tupleArray[i+1]
    dictonary[key] = value

def returnContext(target_num, dic):
    context_indicies = []
    for key in dic:
        if target_num in key:
            if key[0] != target_num:
                if key[0] not in context_indicies:
                    context_indicies.append(key[0])
                else: 
                    if key[1] not in context_indicies:
                        context_indicies.append(key[1])
    return context_indicies

# print(tupleArray)
# print(dictonary)

numNegSamp = 4
print(r.randint(0, len(dictonary)))

def returnNegContext(target_num, dic):
    negContextIndicies = []
    for i in range(5):
        while True:
            negSamp = r.randint(0, len(dictonary))
            a = returnContext(i, dic)
            if not a.__contains__(negSamp):
                negContextIndicies.append(negSamp)
                break
    return negContextIndicies

word_Context_NegContext = []

for word in range(70):
    # print(inverse_vocab[i], returnContext(i, dictonary))
    # print(inverse_vocab[word], word, returnContext(word, dictonary), returnNegContext(word, dictonary))
    word_Context_NegContext.append(inverse_vocab[word])
    word_Context_NegContext.append(returnContext(word, dictonary))
    word_Context_NegContext.append(returnNegContext(word, dictonary))

print(word_Context_NegContext)