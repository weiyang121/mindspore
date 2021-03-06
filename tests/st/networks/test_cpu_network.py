# Copyright 2019 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""
Function: 
    test network
Usage: 
    python test_network_main.py --net lenet --target Davinci
"""
import os
import time
import pytest
import numpy as np
import argparse
import mindspore.nn as nn
from mindspore.common.tensor import Tensor
from mindspore.nn import TrainOneStepCell, WithLossCell
import mindspore.context as context
from mindspore.nn.optim import Momentum
from models.lenet import LeNet
from models.resnetv1_5 import resnet50
from models.alexnet import AlexNet
context.set_context(mode=context.GRAPH_MODE, device_target="CPU")

def train(net, data, label):
    learning_rate = 0.01
    momentum = 0.9

    optimizer = Momentum(filter(lambda x: x.requires_grad, net.get_parameters()), learning_rate, momentum)
    criterion = nn.SoftmaxCrossEntropyWithLogits(is_grad=False, sparse=True)
    net_with_criterion = WithLossCell(net, criterion)
    train_network = TrainOneStepCell(net_with_criterion, optimizer)  # optimizer
    train_network.set_train()
    res = train_network(data, label)
    print("+++++++++Loss+++++++++++++")
    print(res)
    print("+++++++++++++++++++++++++++")
    assert res

@pytest.mark.level0
@pytest.mark.platform_x86_cpu
@pytest.mark.env_onecard
def test_resnet50():
    data = Tensor(np.ones([32, 3 ,224, 224]).astype(np.float32) * 0.01)
    label = Tensor(np.ones([32]).astype(np.int32))
    net = resnet50(32, 10)
    train(net, data, label)

@pytest.mark.level0
@pytest.mark.platform_x86_cpu
@pytest.mark.env_onecard
def test_lenet():
    data = Tensor(np.ones([32, 1 ,32, 32]).astype(np.float32) * 0.01)
    label = Tensor(np.ones([32]).astype(np.int32))
    net = LeNet()
    train(net, data, label)

@pytest.mark.level0
@pytest.mark.platform_x86_cpu
@pytest.mark.env_onecard
def test_alexnet():
    data = Tensor(np.ones([32, 3 ,227, 227]).astype(np.float32) * 0.01)
    label = Tensor(np.ones([32]).astype(np.int32))
    net = AlexNet()
    train(net, data, label)
