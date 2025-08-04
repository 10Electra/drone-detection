import sys, random, shutil, pathlib

"""Make a validation set for training by repurposing a few hundred training images + labels"""

N = int(sys.argv[1])
root = pathlib.Path('datasets/fred_event')

train_imgs = list((root/'images'/'train').glob('*'))
val_img_dir = root/'images'/'val'
val_lbl_dir = root/'labels'/'val'
val_img_dir.mkdir(exist_ok=True)
val_lbl_dir.mkdir(exist_ok=True)

for img in random.sample(train_imgs, N):
    lbl = root/'labels'/'train'/f'{img.stem}.txt'
    shutil.move(img, val_img_dir/img.name)
    shutil.move(lbl, val_lbl_dir/lbl.name)