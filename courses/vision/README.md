# Vision

The track after Zero to Hero: vision foundation models, my research destination (decision of
6 November 2026). Modern vision is transformers plus a few mechanisms of its own, so everything from
Zero to Hero carries over; this track adds what is specific. It starts when lesson 8 is done, and
lesson 9 of Zero to Hero is the bridge: a ViT trained on CIFAR-10 instead of GPT-2.

Sources: Stanford CS231n (https://cs231n.stanford.edu, lectures and assignments public; assignments
2 and 3 once Zero to Hero is done, the earlier ones repeat it); fast.ai part 2, *From Deep Learning
Foundations to Stable Diffusion* (https://course.fast.ai/Lessons/part2.html), diffusion built from
scratch in the same spirit as Karpathy; and the papers below, one folder each in `papers/`.

| # | Folder | What I build | Paper alongside |
|---|---|---|---|
| 01 | `01-convolution` | conv2d by hand (loops, then im2col as one matmul), compared to torch; receptive fields; LeNet on MNIST | LeCun et al. 1998 |
| 02 | `02-resnet` | a small ResNet on CIFAR-10: why residual connections let depth train, measured on the gradient norms with and without | He et al. 2015 (ResNet); Krizhevsky et al. 2012 (AlexNet, for history) |
| 03 | `03-vit` | the GPT block from lesson 7 on image patches: patch embedding, position embeddings, class token; CIFAR-10 | Dosovitskiy et al. 2020 (ViT) |
| 04 | `04-contrastive` | CLIP at toy scale: two encoders, the contrastive loss, zero-shot classification | Radford et al. 2021 (CLIP) |
| 05 | `05-self-supervised` | a masked autoencoder on CIFAR (MAE); DINO's student and teacher if time allows | He et al. 2021 (MAE); Caron et al. 2021 (DINO); Oquab et al. 2023 (DINOv2) |
| 06 | `06-diffusion` | DDPM on MNIST from scratch: the noising process, the ELBO (maths block 03), the U-Net, sampling; then a DiT, the transformer version | Ho et al. 2020 (DDPM); Rombach et al. 2022 (latent diffusion); Peebles and Xie 2023 (DiT) |
| 07 | `07-segment-and-vlm` | reading and small reproductions: SAM, and a VLM (an image encoder feeding a GPT) | Kirillov et al. 2023 (SAM); a VLM paper of the moment |

Compute: MNIST and CIFAR-10 run on the M4; anything ImageNet-sized needs a rented GPU. Same loop as
every lesson: the tutor writes the test, I write the mechanism. A folder appears when I reach it.
