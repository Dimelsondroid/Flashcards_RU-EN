from django.db import models
import pymorphy2
import json

NUM_BOXES = 5
BOXES = range(1, NUM_BOXES + 1)

TYPE_CHOICES = (
    ('noun', 'существительное'),
    ('verb', 'глагол'),
    ('preposition', 'предлог'),
    ('pronoun', 'местоимение'),
    ('adjective', 'прилагательное'),
)


class Card(models.Model):
    WORD_TYPE_CHOICES = {
        'NOUN': ['существительное', 'noun'],
        'ADJF': ['прилагательное', 'adjective'],
        'INFN': ['глагол', 'infinitive'],
        'NUMR': ['числительное', 'numerical'],
        'ADVB': ['наречие', 'adverb'],
        'NPRO': ['местоимение', 'pronoun'],
        'PREP': ['предлог', 'preposition'],
        'CONJ': ['союз', 'conjunction'],
    }

    question = models.CharField(max_length=100, unique=True,
                                help_text='Здесь только русские слова.',
                                error_messages={
                                    'unique': "Такое слово уже существует.",
                                    },
                                )
    answer = models.CharField(max_length=100, unique=True,
                              help_text='Здесь только английские слова.',
                              error_messages={
                                    'unique': "Карточка с таким переводом уже существует.",
                                    },
                              )
    box = models.IntegerField(
        choices=zip(BOXES, BOXES),
        default=BOXES[0],
    )
    word_type = models.CharField(max_length=100, blank=True)
    word_type_ru = models.CharField(max_length=100, blank=True)
    word_type_en = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    def move(self, solved):
        new_box = self.box + 1 if solved else BOXES[0]
        if new_box in BOXES:
            self.box = new_box
            self.save()
        return self

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        morph = pymorphy2.MorphAnalyzer()
        pos = morph.parse(self.question)[0]
        self.word_type = pos.tag.POS
        self.word_type_ru = self.WORD_TYPE_CHOICES[pos.tag.POS][0]
        self.word_type_en = self.WORD_TYPE_CHOICES[pos.tag.POS][1]
        super().save(force_insert=force_insert,
                     force_update=force_update,
                     using=using,
                     update_fields=update_fields, )
        return self

    class Meta:
        verbose_name = 'Карточка'
        verbose_name_plural = "Карточки"
