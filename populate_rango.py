import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                  'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():

    python_pages = [
        {'title': 'Official Python Tutorial',
         'category': 'Python',
         'url': 'http://docs.python.org/3/tutorial/',
         'views': '128',
         'likes': '64',

         },

        {'title': 'How to Think like a Computer Scientist',
         'category': 'Python',
         'url': 'http://www.greenteapress.com/thinkpython/',
         'views': '128',
         'likes': '64',

        },
        {'title': 'Learn Python in 10 Minutes',
         'category': 'Python',
         'url': 'http://www.korokithakis.net/tutorials/python/',
         'views': '128',
         'likes': '64',

         }
        ]
    django_pages = [
        {'title': 'Official Django Tutorial',
         'category': 'Django',
         'url': 'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
         'views': '64',
         'likes': '32',

         },
        {'title': 'Django Rocks',
         'category': 'Django',
         'url':'http://www.djangorocks.com/',
         'views': '64',
         'likes': '32',

         },
        {'title': 'How to Tango with Django',
         'category': 'Django',
         'url': 'http://www.tangowithdjango.com/',
         'views': '64',
         'likes': '32',

         }
    ]
    other_pages = [
        {'title': 'Bottle',
         'category': 'Other Frameworks',
         'url': 'http://bottlepy.org/docs/dev/',
         'views': '32',
         'likes': '16',

         },
        {'title': 'Flask',
         'category': 'Other Frameworks',
         'url': 'http://flask.pocoo.org',
         'views': '32',
         'likes': '16',

         }
    ]
    cats = {'Python': {'pages': python_pages,
                       'views': 128,
                       'likes': 64
                       },
            'Django': {'pages': django_pages,
                       'views': 64,
                       'likes': 32,
                       },
            'Other Frameworks': {'pages': other_pages,
                                 'views': 32,
                                 'likes': 16
                                 }
            }

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])
    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat,title,url,views=0):
  p = Page.objects.get_or_create(category=cat, title=title)[0]

  p.url = url
  p.views = views
  p.save()
  return p
def add_cat(name,views,likes):
  c = Category.objects.get_or_create(name=name)[0]
  c.views = views
  c.likes = likes


  c.save()
  return c
if __name__=='__main__':
    print ('Starting Rango population script...')
    populate()
