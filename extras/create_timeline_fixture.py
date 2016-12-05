import pickle, sys
from twittstopher import Timeline


TIMELINE_USERNAME = 'jack'
NUM_TO_FETCH = 500
print('Fetching {} tweets from twitter for {}'.format(NUM_TO_FETCH, TIMELINE_USERNAME))
tl = Timeline(TIMELINE_USERNAME, NUM_TO_FETCH)

print('Success.. pickling fixture')

with open('test_fixture', 'wb') as fh:
    print('test_fixture opened successfully, writing serialized output')
    pickle.dump(tl, fh, pickle.HIGHEST_PROTOCOL)
    print("Success!")


