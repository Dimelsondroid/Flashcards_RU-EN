from django import template

from cards.models import BOXES, Card

register = template.Library()


@register.inclusion_tag('cards/box_links.html')
def boxes_as_links():
    boxes = []
    for box_num in BOXES:
        card_count = Card.objects.filter(box=box_num).count()
        boxes.append({
            'number': box_num,
            'card_count': card_count,
        })

    return {'boxes': boxes}


@register.inclusion_tag('cards/pos_links.html')
def pos_as_links():
    pos = []
    for item_ru, item_en in Card.WORD_TYPE_CHOICES.values():
        pos_count = Card.objects.filter(word_type_en=item_en).count()
        pos.append({
            'pos_ru': item_ru,
            'pos_en': item_en,
            'pos_count': pos_count,
        })
    return {'pos': pos}
