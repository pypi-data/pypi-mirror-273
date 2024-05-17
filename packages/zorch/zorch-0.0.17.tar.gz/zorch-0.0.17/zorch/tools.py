


from matplotlib import pyplot as plt


def display_data(dataloader, class_names,hw=[1,5]):
    images, labels = next(iter(dataloader["train"]))    
    fig, axes = plt.subplots(hw[0],hw[1],figsize=(15, 6))  # 调整图像尺寸以避免图像被压缩得太小
    axes = axes.flatten()  # 将axes数组展平为一维数组
    for i in range(hw[0]*hw[1]):  # 确保不超过轴对象的数量
        axes[i].imshow(images[i].permute(1, 2, 0))  # 改变维度顺序
        axes[i].set_title(class_names[labels[i]])
        axes[i].axis('off')
    plt.show()