# Webspam-detection-based-on-machine-learning

####在DataAcquire文件夹下是一些用于获取网页的模块，具体如下:

 1.main.py是程序入口，可以通过运行此文件获取到所有网页内容并存储到磁盘上

 2.ReadConf.py是读取配置文件。配置文件主要有输入路径，输出路径和错误路径

 3.SaveDataInFile是将html存入到指定路径的文件中

 4.GetHtmlData是向链接发送get请求获取目标网页内容

 5.FileNameGenerator是将网页链接中不符合操作系统命名规范的字符替换

 6.HtmlCOntentGetter是获取到html中的文本内容包括只有中文或者所有文本内容

 7.URLExtractor是使用FileNameGenerator来根据html链接生成符合操作系统命名规范的文件名，并且可以通过文件名将html链接还原出来

 #####DataAcquire主要使用方法
 在ExperimentSample是数据集及数据集处理的中间数据。其中杨望老师提供了由原来的关键词匹配算法爬取的网页链接集合两个，分别是DataSource和DataSource1,
 将这两个文件夹中的文件输入到这个main.py中可以爬取到其中html内容并存储到HtmlSource和HtmlSource1,如果遇到网页错误或者没有这个网页等问题会输出到Errors文件夹，里面的内容是问题原因。
 通过这样我们就获取到了网页内容，我们将基于这些数据进行训练和测试

####在DataPreprocessAndJudge文件下是用于处理数据并且检测学习的模块。具体如下:

 1.HtmlBlockSeparator模块是网页分块模块，对网页进行分块，并存入文件系统

 2.TagArrayGenerator模块是对目标网页标签进行处理，生成标签的特征矩阵

 3.HeadArrayGenerator模块是对目标网页头部进行处理，生成头部的特征矩阵

 4.AttributeArrayGenerator模块是对目标网页叶标签属性进行处理，生成属性的特征矩阵

 5.TextArrayGenerator模块是对目标网页标签文本内容进行处理，返回文本内容的平均优势率

 6.AllArrayGenerator模块是调用12345模块，将训练数据分块后生成的特征向量存入磁盘并生成初始化的网页结构的机器学习模型

 7.TextAnalysis模块是用初始数据初始化优势率字典

 8.NewHtmlJudgeAndLearning是检测和学习模块，对于新的网页数据进行检测和学习，将分类结果存入文件系统

 9.RightRatioTest模块是将测试数据算法分类结果和人工分类结果比较，计算正确率。

 ##### DataPreprocessAndJudge主要使用方法

 这部分是核心部分，其实分为两个部分，第一部分是训练，第二部分是输入新数据测试准确率和误报率，
 第一部分的入口是AllArrayGenerator和TextAnalysis两个，
 其中AllArrayGenrator 是调用12345模块，将训练数据分块后生成的特征向量存入磁盘并生成初始化的网页结构的机器学习模型。
 首先使用其中的main函数生成特征向量并存入磁盘，其中有一段svc的code可以忽略，那个是我之前用来测试svc的。需要做的是把那些main函数相关的注释取消掉，
 把与其不相关的注释掉。
 然后使用其中的
 nb_clf = MultinomialNB()  # MultinomialNB的参数设置可以参考sklearn官网
 minibatch_train_iterators = iter_minibatches(ArrayDataCSVFilePath, minibatch_size=5000)
 for i, (X_train, y_train) in enumerate(minibatch_train_iterators):
使用 partial_fit ，并在第一次调用 partial_fit 的时候指定 classes

​      nb_clf.partial_fit(X_train, y_train, classes=np.array([0, 1]))
​      print("{} time".format(i))  # 当前次数

 print("{} score".format(nb_clf.score(X_test, y_test)))  # 在测试集上看效果

 joblib.dump(nb_clf, ModelFilePath)
 这段来将arraydata用MultinomialNB的机器学习算法结合增量学习将之前生成的array数据生成机器学习模型。这边你要做的也是把这段相关的注释取消掉，无关的注释掉。
 这段确实存在问题，可以将生成模型的这段单独封装出来更好。

 TextAnalysis是用来初始化优势率字典，
 以上两个所用的数据路径及生成的数据路径可以从代码中看出。
 对于这两个的调用没有先后之分，因为他们互不影响。
 第二部分的入口是NewHtmlJudgeAndLearning和RightRatioTest。NewHtmlJudgeAndLearning是检测和学习模块，对于新的网页数据进行检测和学习，将分类结果存入文件系统。
 RightRatioTest模块是将测试数据算法分类结果和人工分类结果比较，计算正确率。你可以从代码中看出所用数据路径和生成的数据路径。这两个应该先调用NewHtmlJudgeAndLearning生成结果后
 再调用RightRatioTest去测试正确率和误报率，具体方法可以从代码中看出

其余的部分比如12345都是中间过程部分，具体思路可以看代码和论文。
