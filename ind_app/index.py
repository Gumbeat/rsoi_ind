from tqdm import tqdm
import os


class Singleton(object):
    _instances = {}

    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
        return class_._instances[class_]


class Index(Singleton):
    vowels = "аеиоуыеюя"

    def __init__(self):
        self.word_dict = {}

    @staticmethod
    def procesString(string):
        tmp = string
        tmp.replace("  ", " ")
        tmp = tmp.split()

        return [tmp[i] for i in range(0, len(tmp), 2)]

    def findeRV_R1_R2(self, word):
        ptr = 0
        ans = {"RV": len(word), "R1": len(word) + 1, "R2": len(word) + 1}

        for i in range(ptr, len(word)):
            if word[i] in self.vowels:
                ptr += 1
                ans["RV"] = ptr
                break
            ptr += 1

        for i in range(ptr, len(word)):
            if word[i] not in self.vowels:
                ptr += 1
                ans["R1"] = ptr
                break
            ptr += 1

        for i in range(ptr, len(word)):
            if word[i] in self.vowels:
                ptr += 1
                break
            ptr += 1

        for i in range(ptr, len(word)):
            if word[i] not in self.vowels:
                ptr += 1
                ans["R2"] = ptr
                break
            ptr += 1

        return ans

    def StemSTEP1(self, word, RV_R1_R2):
        max_w = ""

        for i in PERFECTIVE_GERUND[0]:
            if (word.find("а" + i, RV_R1_R2["RV"]) != -1 or
                    word.find("я" + i, RV_R1_R2["RV"]) != -1):
                if len(i) > len(max_w):
                    max_w = i

        for i in PERFECTIVE_GERUND[1]:
            if word.find(i, RV_R1_R2["RV"]) != -1:
                if len(i) > len(max_w):
                    max_w = i

        if max_w != "":
            return word[:-len(max_w)]

        max_w = ""
        for i in REFLEXIVE:
            if word.find(i, RV_R1_R2["RV"]) != -1:
                if len(i) > len(max_w):
                    max_w = i

        if max_w != "":
            word = word[:-len(max_w)]

        max_w = ""
        for i in ADJECTIVE:
            if word.find(i, RV_R1_R2["RV"]) != -1:
                if len(i) > len(max_w):
                    max_w = i

        for i in PARTICIPLE[0]:
            for j in ADJECTIVE:
                if (word.find("а" + i + j, RV_R1_R2["RV"]) != -1 or
                        word.find("я" + i + j, RV_R1_R2["RV"]) != -1):
                    if len(i + j) > len(max_w):
                        max_w = i + j

        for i in PARTICIPLE[1]:
            for j in ADJECTIVE:
                if word.find(i + j, RV_R1_R2["RV"]) != -1:
                    if len(i + j) > len(max_w):
                        max_w = i + j

        if max_w != "":
            return word[:-len(max_w)]

        max_w = ""

        for i in VERB[0]:
            if (word.find("а" + i, RV_R1_R2["RV"]) != -1 or
                    word.find("я" + i, RV_R1_R2["RV"]) != -1):
                if len(i) > len(max_w):
                    max_w = i

        for i in VERB[1]:
            if word.find(i, RV_R1_R2["RV"]) != -1:
                if len(i) > len(max_w):
                    max_w = i

        if max_w != "":
            return word[:-len(max_w)]

        max_w = ""
        for i in NOUN:
            if word.find(i, RV_R1_R2["RV"]) != -1:
                if len(i) > len(max_w):
                    max_w = i

        if max_w != "":
            return word[:-len(max_w)]

        return word

    def StemSTEP2(self, word):
        if word[-1] == 'и':
            return word[:-1]
        return word

    def StemSTEP3(self, word, RV_R1_R2):
        max_w = ""
        for i in DERIVATIONAL:
            if word.find(i, RV_R1_R2["RV"]) != -1:
                if len(i) > len(max_w):
                    max_w = i

        if max_w != "":
            return word[:-len(max_w)]
        return word

    def StemSTEP4(self, word, RV_R1_R2):
        max_w = ""
        for i in SUPERLATIVE:
            if word.find(i, RV_R1_R2["R2"]) != -1:
                if len(i) > len(max_w):
                    max_w = i

        if max_w != "":
            word = word[:-len(max_w)]

        if word.find("нн", RV_R1_R2["RV"]) != -1:
            i = word.find("нн", RV_R1_R2["RV"])
            word = word[:i]

        if word[-1] == "ь":
            word = word[:-1]
        return word

    def Stem(self, word):
        if len(word) < 2:
            return word

        RV_R1_R2 = self.findeRV_R1_R2(word)

        word = self.StemSTEP1(word, RV_R1_R2)
        word = self.StemSTEP2(word)
        word = self.StemSTEP3(word, RV_R1_R2)
        word = self.StemSTEP4(word, RV_R1_R2)
        return word

    punctuation_marks = [',', '.', '[', ']', '(', ')', ':', '!', '?', '́', '—', '-', '«', '»']

    def replace_punctuation(self, line):
        for mark in self.punctuation_marks:
            line = line.replace(mark, '')
        return line

    # filename = input('Введите название файла: ')
    # if __name__ == '__main__':

    def rebuild(self):
        self.word_dict = {}
        folder_path = 'G:\\постметаластовый\\РСОИ\\individualka\\ind_app\\documents'
        folder_name = 'documents\\'
        all_files = os.listdir(folder_path)
        txt_files = filter(lambda x: x[-4:] == '.txt', all_files)
        basepath = os.path.dirname(__file__)
        for filename in txt_files:
            filepath = os.path.abspath(os.path.join(basepath, f'{folder_name}{filename}'))
            with open(filepath, encoding='utf-8') as f:
                content = f.readlines()
            for line in content:
                formatted_line = self.replace_punctuation(line).replace('  ', ' ').strip()
                if len(formatted_line) <= 0:
                    continue
                words = formatted_line.split(' ')
                for word in words:
                    stem_word = self.Stem(word)
                    if stem_word not in self.word_dict:
                        self.word_dict[stem_word] = set()
                    self.word_dict[stem_word].add(filename)

            for word, documents in self.word_dict.items():
                print(f'Слово: {word}. Документы: {documents}')

    def get_word_dict(self):
        if not self.word_dict:
            self.rebuild()
        return self.word_dict


PERFECTIVE_GERUND = [["в", "вши", "вшись"],
                     ["ив", "ивши", "ившись", "ыв", "ывши", "ывшись"]]
ADJECTIVE = Index.procesString(
    "ее (ee)   ие (ie)   ые (ye)   ое (oe)   ими (imi)   ыми (ymi)   ей (eì)   ий (iì)   ый (yì)   ой (oì)   ем (em)   им (im)   ым (ym)   ом (om)   его (ego)   ого (ogo)   ему (emu)   ому (omu)   их (ikh)   ых (ykh)   ую (uiu)   юю (iuiu)   ая (aia)   яя (iaia)   ою (oiu)   ею (eiu)")
PARTICIPLE = [Index.procesString("ем (em)   нн (nn)   вш (vsh)   ющ (iushch)   щ (shch)"),
              Index.procesString("ивш (ivsh)   ывш (yvsh)   ующ (uiushch)")]
REFLEXIVE = Index.procesString("ся (sia)   сь (s')")
VERB = [Index.procesString(
    "ла (la)   на (na)   ете (ete)   йте (ìte)   ли (li)   й (ì)   л (l)   ем (em)   н (n)   ло (lo)   но (no)   ет (et)   ют (iut)   ны (ny)   ть (t')   ешь (esh')   нно (nno)"),
    Index.procesString(
        "ила (ila)   ыла (yla)   ена (ena)   ейте (eìte)   уйте (uìte)   ите (ite)   или (ili)   ыли (yli)   ей (eì)   уй (uì)   ил (il)   ыл (yl)   им (im)   ым (ym)   ен (en)   ило (ilo)   ыло (ylo)   ено (eno)   ят (iat)   ует (uet)   уют (uiut)   ит (it)   ыт (yt)   ены (eny)   ить (it')   ыть (yt')   ишь (ish')   ую (uiu)   ю (iu)")]
NOUN = Index.procesString(
    "а (a)   ев (ev)   ов (ov)   ие (ie)   ье ('e)   е (e)   иями (iiami)   ями (iami)   ами (ami)   еи (ei)   ии (ii)   и (i)   ией (ieì)   ей (eì)   ой (oì)   ий (iì)   й (ì)   иям (iiam)   ям (iam)   ием (iem)   ем (em)   ам (am)   ом (om)   о (o)   у (u)   ах (akh)   иях (iiakh)   ях (iakh)   ы (y)   ь (')   ию (iiu)   ью ('iu)   ю (iu)   ия (iia)   ья ('ia)   я (ia)")
SUPERLATIVE = Index.procesString("ейш (eìsh)   ейше (eìshe)")
DERIVATIONAL = Index.procesString("ост (ost)   ость (ost')")

index = Index()
