# Multi-task-classification-on-celebA-dataset
Multi task classification on celebA dataset

These are the attributes I selected:
'Wearing_Earrings', 'Wearing_Necklace', 'Big_Lips',
'High_Cheekbones', 'Arched_Eyebrows', 'Heavy_Makeup',
'Smiling', 'Young'
Reason:
I selected these attributes because they are
somehow more related to each other. So, while
calculating dropout, you will get reasonable values and
know which ones have less weightage among them in a
certain task. All of them are related to the face.

Backbone: ResNet18
Reasons:
1)ResNet18 has residual connections, which will help it
perform deeper tasks with less computation than
VGG16 .since we are dealing with celebA dataset,
which is very large. We fewer computation
resources, I used ResNet18.
2) ResNet18's architecture is designed to be more
adaptable to different data types and tasks, while
VGG16's architecture is more specific to image
classification.
Parameters:
Learning rate = 0.01 is used in Adam optimizer
Scheduler (step size =3): The learning rate scheduler
adjusts the learning rate during training to help the
model converge faster and more accurately. We used
step size =3 This means it reduces the learning rate by 10
every 3 epochs. This can help the model converge faster
and avoid overshooting the optimal solution.


![image](https://github.com/akash1akash1/Multi-task-classification-on-celebA-dataset/assets/128292061/bdc36e10-32ae-4272-9af0-ad8980adaef9)

