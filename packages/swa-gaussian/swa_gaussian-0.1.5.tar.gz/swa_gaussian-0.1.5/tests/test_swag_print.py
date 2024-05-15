
import torch
import numpy as np
import unittest
import sys

import gpytorch
from numpy.testing import assert_array_equal

from swag.posteriors import SWAG


class TestSWAG(unittest.TestCase):

    input_size = 8
    output_size = 2

    def test_string_representation(self):
        model = torch.nn.Linear(self.input_size, self.output_size, bias=True)
        self.swag_model = SWAG(
            torch.nn.Linear,
            in_features=self.input_size,
            out_features=self.output_size,
            bias=True,
            no_cov_mat=False,
            max_num_models=10,
            device='cpu'
        )
        # empty swag model
        print("[Initial, SWAG] " + str(self.swag_model))
        print("[Initial, base] " + str(self.swag_model.base))
        out1 = self.swag_model.forward(torch.randn(5, self.input_size))
        print("Out: %s" % out1)

        # construct swag model via training
        optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)
        torch.manual_seed(0)
        for _ in range(101):
            model.zero_grad()
            input = torch.randn(100, self.input_size)
            output = model(input)
            loss = ((torch.randn(100, self.output_size) - output) ** 2.0).sum()
            loss.backward()
            optimizer.step()
            self.swag_model.collect_model(model)
        print("[Trained, SWAG] " + str(self.swag_model))
        print("[Trained, base] " + str(self.swag_model.base))
        out2 = self.swag_model.forward(torch.randn(5, self.input_size))
        print("Out: %s" % out2)
        assert_array_equal(out1, out2)

        # sample base model parameters
        self.swag_model.sample()
        print("[Final, SWAG] " + str(self.swag_model))
        print("[Final, base] " + str(self.swag_model.base))
        out3 = self.swag_model.forward(torch.randn(5, self.input_size))
        print("Out: %s" % out3)
        with self.assertRaises(AssertionError):
            assert_array_equal(out2, out3)


if __name__ == "__main__":
    unittest.main()
