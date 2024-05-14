# moModelAnalysisTool
## 准备工作
```
pip install pqi
pqi use pypi 
pip install momodeltool / pip install momodeltool --upgrade
```
## Visualization模块
通道可视化模块，使用举例：  
```python
from momodeltool import Visualization

'''使用开关'''
def forward(self, x):
  out = layer1(x)
  visual = Visualization()
  visual.switch_control()  # 打开展示开关，展示layer1
  visual.show_layer(out, module_name='layer1', show=True, save='./', pseudo=True, hist=True)
  visual.switch_control()  # 关闭展示开关，不展示layer2
  visual.show_layer(out, module_name='layer2', show=True, save='./', pseudo=True, hist=True) 
  out = layer2(out)
  visual.destroyAllWindows()  # 任意键入，关闭所有窗口

'''使用静态方法'''
def forward(self, x):
  out = layer1(x)
  Visualization.layer_show(out, module_name='layer1', show=True, save='./', pseudo=True, hist=True, norm=True, mode=2)  # 展示layer1，任意键入，关闭相关窗口 norm归一话开关 mode=1归一化针对展示的全图，mode=2归一化针对全图中的单个图像
  out = layer2(out)

model.load_state_dict()
Visualization.kernel_show(model, module_name='test', show=Ture, save='./')
```
展示样例  
![Alt text](demo/image_hist.png)
![Alt text](demo/image.png)
## ModelProcess模块
网络模型处理模块，使用样例：  
```python
from momodeltool import ModelProcess

mp = ModelProcess()
model = stereonet(batch_size=1, cost_volume_method=cost_volume_method)
pretrained_model_path = "mypath/model_1340.pth"
new_model = mp.auto_adapt(model, pretrained_model_path)  # 自动调整权重
mp.show_keys(new)  # 展示模型权重key
```