import pandas as pd
from math import sqrt
from matplotlib import pyplot
from statsmodels.tsa.vector_ar.var_model import VAR
from sklearn.metrics import mean_squared_error

data = pd.read_csv("data.csv", index_col=False)

train = data[:int(0.8*(len(data)))]
valid = data[int(0.8*(len(data))):]

model = VAR(endog=train)
model_fit = model.fit(maxlags=15)
print model_fit.summary()
model_fit.plot()

prediction = model_fit.forecast(model_fit.y, steps=len(valid))
model_fit.plot_forecast(len(valid))

cols = data.columns

#converting predictions to dataframe
pred = pd.DataFrame(index=range(0,len(prediction)),columns=[cols])
for j in range(0,4):
    for i in range(0, len(prediction)):
       pred.iloc[i][j] = prediction[i][j]

#check rmse
for i in cols:
    print('rmse value for', i, 'is : ', sqrt(mean_squared_error(pred[i], valid[i])))

"""
size = int(len(X) * 0.66)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()
for t in range(len(test)):
	model = ARIMA(history, order=(5,1,0))
	model_fit = model.fit(disp=0)
	output = model_fit.forecast()
	yhat = output[0]
	predictions.append(yhat)
	obs = test[t]
	history.append(obs)
	print('predicted=%f, expected=%f' % (yhat, obs))
error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)
# plot
pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.show()
"""
