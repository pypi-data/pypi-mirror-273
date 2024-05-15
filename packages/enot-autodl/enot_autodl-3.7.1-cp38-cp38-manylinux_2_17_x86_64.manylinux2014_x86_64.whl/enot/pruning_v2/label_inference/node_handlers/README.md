### TORCH

###### Conv

- [x] `torch.nn.functional.conv1d`
- [x] `torch.nn.functional.conv2d`
- [x] `torch.nn.functional.conv3d`
- [x] `torch.nn.functional.conv_transpose1d`
- [x] `torch.nn.functional.conv_transpose2d`
- [x] `torch.nn.functional.conv_transpose3d`

###### Linear

- [x] `torch.nn.function.linear`

###### Matmul

- [x] `torch.matmul`
- [x] `torch.Tensor.matmul`
- [x] `torch.linalg.matmul`
- [x] `torch.mv`
- [x] `torch.Tensor.mv`
- [x] `torch.mm`
- [x] `torch.Tensor.mm`
- [x] `torch.bmm`
- [x] `torch.Tensor.bmm`
- [x] `@`

###### Concat

- [x] `torch.cat`
- [x] `torch.concat`

###### Permute

- [x] `torch.permute`
- [x] `torch.Tensor.permute`

###### Transpose

- [x] `torch.transpose`
- [x] `torch.Tensor.transpose`
- [x] `torch.Tensor.transpose_`
- [x] `torch.t`
- [x] `torch.Tensor.t`
- [x] `torch.Tensor.t_`
- [x] `torch.Tensor.T`
- [x] `torch.Tensor.mT`

###### Expand

- [x] `torch.Tensor.expand`
- [x] `torch.Tensor.expand_as`

###### Reshape

Only the "flatten" case is implemented: multiple dimensions to single dimension.

- [x] `torch.reshape`
- [x] `torch.Tensor.reshape`
- [x] `torch.view`
- [x] `torch.Tensor.view`
- [x] `torch.flatten`
- [x] `torch.Tensor.flatten`
- [ ] `torch.unsqueeze`
- [ ] `torch.Tensor.unsqueeze`
- [ ] `torch.Tensor.unsqueeze_`
- [ ] `torch.Tensor.reshape_as`
- [ ] `torch.Tensor.view_as`

###### Where

- [x] `torch.where`
- [x] `torch.Tensor.where`

###### GetItem

- [x] `operator.getitem`

###### Detach

- [x] `torch.Tensor.detach`
- [ ] `torch.Tensor.detach_` - RuntimeError: Can't detach views in-place. Use detach() instead.
- [x] `torch.detach`
- [ ] `torch.detach_` - RuntimeError: Can't detach views in-place. Use detach() instead.

###### LayerNorm

- [x] `torch.nn.functional.layer_norm`

###### Matmul with Addition

- [x] `torch.addmm`
- [x] `torch.Tensor.addmm`
- [x] `torch.Tensor.addmm_`
- [x] `torch.addbmm`
- [x] `torch.Tensor.addbmm`
- [x] `torch.Tensor.addbmm_`
- [x] `torch.addmv`
- [x] `torch.Tensor.addmv`
- [x] `torch.Tensor.addmv_`
- [x] `torch.baddbmm`
- [x] `torch.Tensor.baddbmm`
- [x] `torch.Tensor.baddbmm_`

###### GRU

- [ ] `torch.gru`

###### LSTM

- [ ] `torch.lstm`

###### Embedding

- [x] `torch.nn.functional.embedding`

#### Reduce operations

- [x] `argmax`
- [x] `argmin`
- [x] `amax`
- [x] `amin`
- [x] `all`
- [x] `any`
- [x] `logsumexp`
- [x] `mean`
- [x] `nanmean`
- [x] `norm`
- [x] `nansum`
- [x] `prod`
- [x] `std`
- [x] `sum`
- [x] `var`

#### Droupout operations

- [x] `torch.nn.functional.dropout`
- [x] `torch.nn.functional.dropout2d`
- [x] `torch.nn.functional.dropout3d`
- [x] `torch.nn.functional.alpha_dropout`
- [x] `torch.nn.functional.feature_alpha_dropout`

#### Elementwise operations

##### Activations

- [x] `celu`
- [x] `celu_`
- [x] `elu`
- [x] `elu_`
- [x] `gelu`
- [x] `glu`
- [x] `hardshrink`
- [x] `hardsigmoid`
- [x] `hardswish`
- [x] `hardtanh`
- [x] `hardtanh_`
- [x] `leaky_relu`
- [x] `leaky_relu_`
- [x] `logsigmoid`
- [x] `log_softmax`
- [x] `mish`
- [x] `relu`
- [x] `relu_`
- [x] `relu6`
- [x] `rrelu`
- [x] `rrelu_`
- [x] `selu`
- [x] `selu_`
- [x] `sign`
- [x] `sign_`
- [x] `expit`
- [x] `sigmoid`
- [x] `sigmoid_`
- [x] `silu`
- [x] `softmax`
- [x] `softmin`
- [x] `softplus`
- [x] `softshrink`
- [x] `softsign`
- [x] `tanh`
- [x] `tanh_`
- [x] `tanhshrink`

##### Functions

- [x] `abs`
- [x] `abs_`
- [x] `absolute`
- [x] `absolute_`
- [x] `acos`
- [x] `acos_`
- [x] `acosh`
- [x] `acosh_`
- [x] `arccos`
- [x] `arccos_`
- [x] `arccosh`
- [x] `arccosh_`
- [x] `arcsin`
- [x] `arcsin_`
- [x] `arcsinh`
- [x] `arcsinh_`
- [x] `arctan`
- [x] `arctan_`
- [x] `arctanh`
- [x] `arctanh_`
- [x] `asin`
- [x] `asin_`
- [x] `asinh`
- [x] `asinh_`
- [x] `atan`
- [x] `atan_`
- [x] `atanh`
- [x] `atanh_`
- [x] `ceil`
- [x] `ceil_`
- [x] `clamp`
- [x] `clamp_`
- [x] `clip`
- [x] `clip_`
- [x] `cos`
- [x] `cos_`
- [x] `cosh`
- [x] `cosh_`
- [x] `erf`
- [x] `erf_`
- [x] `erfc`
- [x] `erfc_`
- [x] `erfinv`
- [x] `erfinv_`
- [x] `exp`
- [x] `exp_`
- [x] `exp2`
- [x] `exp2_`
- [x] `expm1`
- [x] `expm1_`
- [x] `floor`
- [x] `floor_`
- [x] `log`
- [x] `log_`
- [x] `log10`
- [x] `log10_`
- [x] `log1p`
- [x] `log1p_`
- [x] `log2`
- [x] `log2_`
- [x] `logit`
- [x] `logit_`
- [x] `neg`
- [x] `neg_`
- [x] `negative`
- [x] `negative_`
- [x] `normalize`
- [x] `pow`
- [x] `pow_`
- [x] `round`
- [x] `round_`
- [x] `rsqrt`
- [x] `rsqrt_`
- [x] `sin`
- [x] `sin_`
- [x] `sinc`
- [x] `sinc_`
- [x] `sinh`
- [x] `sinh_`
- [x] `sqrt`
- [x] `sqrt_`
- [x] `square`
- [x] `square_`
- [x] `tan`
- [x] `tan_`
- [x] `trunc`
- [x] `trunc_`

#### Channelwise operations

- [x] `torch.nn.functional.adaptive_avg_pool1d`
- [x] `torch.nn.functional.adaptive_max_pool1d`
- [x] `torch.nn.functional.adaptive_avg_pool2d`
- [x] `torch.nn.functional.adaptive_max_pool2d`
- [x] `torch.nn.functional.adaptive_avg_pool3d`
- [x] `torch.nn.functional.adaptive_max_pool3d`
- [x] `torch.nn.functional.avg_pool1d`
- [x] `torch.nn.functional.max_pool1d`
- [x] `torch.nn.functional.avg_pool2d`
- [x] `torch.nn.functional.max_pool2d`
- [x] `torch.nn.functional.avg_pool3d`
- [x] `torch.nn.functional.max_pool3d`
- [x] `torch.nn.functional.upsample`
- [x] `torch.nn.functional.upsample_nearest`
- [x] `torch.nn.functional.upsample_bilinear`
- [x] `torch.nn.functional.max_unpool1d`
- [x] `torch.nn.functional.max_unpool2d`
- [x] `torch.nn.functional.max_unpool3d`
- [x] `torch.nn.functional.interpolate`
- [x] `torch.nn.functional.pad`
- [x] `torch.nn.functional.grid_sample`
- [x] `torch.nn.functional.batch_norm`
- [x] `torch.nn.functional.instance_norm`
- [x] `torch.nn.functional.prelu`

#### Binary elementwise operations

Aggregate operations subset

- [x] `operator.add`
- [x] `operator.iadd`
- [x] `operator.sub`
- [x] `operator.isub`
- [x] `operator.mul`
- [x] `operator.imul`
- [x] `operator.truediv`
- [x] `operator.itruediv`
- [x] `add`
- [x] `add_`
- [x] `sub`
- [x] `sub_`
- [x] `subtract`
- [x] `subtract_`
- [x] `mul`
- [x] `mul_`
- [x] `multiply`
- [x] `multiply_`
- [x] `div`
- [x] `div_`
- [x] `divide`
- [x] `divide_`
- [x] `true_divide`
- [x] `true_divide_`

Comparison operations subset

- [x] `operator.eq`
- [x] `operator.ne`
- [x] `operator.le`
- [x] `operator.ge`
- [x] `operator.lt`
- [x] `operator.gt`
- [x] `operator.pow`
- [x] `operator.ipow`
- [x] `eq`
- [x] `eq_`
- [x] `ne`
- [x] `ne_`
- [x] `not_equal`
- [x] `not_equal_`
- [x] `le`
- [x] `le_`
- [x] `less_equal`
- [x] `less_equal_`
- [x] `ge`
- [x] `ge_`
- [x] `greater_equal`
- [x] `greater_equal_`
- [x] `lt`
- [x] `lt_`
- [x] `less`
- [x] `less_`
- [x] `gt`
- [x] `gt_`
- [x] `greater`
- [x] `greater_`

All other binary operations

- [x] `pow`
- [x] `pow_`

#### Block operations

- [ ] `_VariableFunctionsClass._cudnn_rnn_flatten_weight`
- [x] `torch.get_device`
- [x] `torch.is_floating_point`
- [x] `torch.Tensor.data_ptr`
- [x] `torch.Tensor.dim`
- [x] `torch.Tensor.is_floating_point`
- [x] `torch.Tensor.get_device`
- [x] `torch.Tensor.shape`
- [x] `torch.Tensor.size`
- [x] `torch.Tensor.type`

#### Bypass operations

- [x] `float`
- [x] `double`
- [x] `half`
- [x] `bfloat16`
- [x] `cdouble`
- [x] `short`
- [x] `int`
- [x] `long`
- [x] `bool`
- [x] `torch.Tensor.contiguous`
- [x] `torch.Tensor.cpu`
- [x] `torch.Tensor.cuda`
- [x] `torch.Tensor.to`
