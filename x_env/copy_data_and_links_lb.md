readme 昨天没有做到镜像里，直接贴出来你看下吧
* 使用webui前请先确保autodl-tmp下正确的拷贝了models, training, outputs这几个目录

如果在内蒙区的话，可以从autodl-fs/albert-models下复制到autodl-tmp下。
cp -r ~/autodl-fs/albert-models/models ~/autodl-tmp
mkdir ~/autodl-tmp/outputs

如果不在内蒙区，可以参考跨区拷贝
scp -rP <某内蒙区机器的PORT> root@connect.neimeng.seetacloud.com:/root/autodl-fs/albert-models/models ~/autodl-tmp
mkdir ~/autodl-tmp/outputs

[启动 Automatic1111(webui)]
在终端输入如下指令
cd ~/stable-diffusion-webui
./webui.sh --share

[Lora训练]
1. 编辑~/alex-trainer/train_lora.py 设置训练参数
2. 运行以下命令开始训练
cd ~/alex-trainer
python train_lora.py