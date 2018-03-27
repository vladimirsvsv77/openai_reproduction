from encoder import Model
from matplotlib import pyplot as plt
from utils import sst_binary, train_with_reg_cv
import numpy as np
import os

model = Model('/Users/jonathan/Desktop/openai_reproduction_repo/model/994/model.npy')

trX, vaX, teX, trY, vaY, teY = sst_binary()

if not os.path.exists('features/amazon'):
    os.makedirs('features/amazon')

    trXt = model.transform(trX)
    vaXt = model.transform(vaX)
    teXt = model.transform(teX)

    np.save('features/amazon/trXt',trXt)
    np.save('features/amazon/vaXt',vaXt)
    np.save('features/amazon/teXt',teXt)

else:
    print('load features')
    trXt = np.load('features/amazon/trXt.npy')
    vaXt = np.load('features/amazon/vaXt.npy')
    teXt = np.load('features/amazon/teXt.npy')


# delete sentiment neuron
# trXt[:, 3984]=0
# vaXt[:, 3984]=0
# teXt[:, 3984]=0

#only sentiment neuron
trXt[0:3984, 3985:]=0
vaXt[0:3984, 3985:]=0
teXt[0:3984, 3985:]=0



full_rep_acc, c, nnotzero, coef, lg_model = train_with_reg_cv(trXt, trY, vaXt, vaY, teXt, teY)
print('%05.2f test accuracy'%full_rep_acc)
print('%05.2f regularization coef'%c)
print('%05d features used'%nnotzero)

# visualize sentiment unit
sentiment_unit = trXt[:, 3984]
plt.hist(sentiment_unit[trY==0], bins=25, alpha=0.5, label='neg')
plt.hist(sentiment_unit[trY==1], bins=25, alpha=0.5, label='pos')
plt.legend()
plt.show()
