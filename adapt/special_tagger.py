class NumTagger:
    def __init__(self):
        pass

    def match(self, tokens):
        print(tokens)
        entities = []
        for idx in range(len(tokens)):
            part = ' '.join(tokens[idx:])
            # print(part)
            res = self.text2int(part)
            # new_entity['data'] = list(new_entity['data'])
            # print(res)
            if res:
                new_entity = {
                    'confidence': 1.0,
                    'data': [(res, 'numeric')],
                    'key': part,
                    'match': part
                }
                entities.append({
                    'match': part,
                    'key': "numeric",
                    'start_token': idx,
                    'entities': [new_entity],
                    'value': res,
                    'end_token': idx
                })

        return entities


    def text2int(self, textnum, numwords={}):
        # from StackOverflow:
        # http://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers
        if not numwords:
          units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
          ]

          tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

          scales = ["hundred", "thousand", "million", "billion", "trillion"]

          numwords["and"] = (1, 0)
          for idx, word in enumerate(units):    numwords[word] = (1, idx)
          for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
          for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

        current = result = 0
        is_match = False
        for word in textnum.split():
            if word not in numwords:
                break
            is_match = True
            scale, increment = numwords[word]
            current = current * scale + increment

            if scale > 100:
                result += current
                current = 0

        if is_match:
            return result + current
        else:
            return None

class DateTimeTagger:
    def __init__(self):
        pass

    def match(self, tokens):
        print(tokens)
        entities = []
        for idx in xrange(len(tokens)):
            part = ' '.join(tokens[idx:])
            print(part)
            res = self.text2int(part)
            # new_entity['data'] = list(new_entity['data'])
            print(res)
            if res:
                new_entity = {
                    'confidence': 1.0,
                    'data': [(res, 'NUMERIC')],
                    'key': part,
                    'match': part
                }
                entities.append({
                    'match': part,
                    'key': "NUMERIC VALUE",
                    'start_token': idx,
                    'entities': [new_entity],
                    'value': res,
                    'end_token': idx + 1
                })
        return entities

