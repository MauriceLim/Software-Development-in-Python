import pytest
from vasicek import VasicekModel
from vasicek import Bondoptions

# Create a Vasicek model instance with the given parameters
a = 0.1
b= 0.08
r0 = 0.05
sigma = 0.015
TO = 1
TB = 3
K = 0.87

model = VasicekModel(a, b, r0, sigma)

# Define the expected results
expected_mean_5 = 0.06180408020862101
expected_variance_5 = 0.0007111356286821274
SZ = 0.02588585159177525
d1 = 1.142766967386068
d2 = 1.1168811157942928
V_call = 0.025929830615982197
V_put = 0.001403706405088287

def test_mean():
    assert pytest.approx(model.mean(5), abs=1e-6) == expected_mean_5

def test_variance():
    assert pytest.approx(model.var(5), abs=1e-6) == expected_variance_5

def test_SZ():
    assert pytest.approx(Bondoptions(model,TO,TB,K).sz(), abs=1e-6) == SZ

def test_d1():
    assert pytest.approx(Bondoptions(model,TO,TB,K).d1(), abs=1e-6) == d1

def test_d2():
    assert pytest.approx(Bondoptions(model,TO,TB,K).d2(), abs=1e-6) == d2

def test_Vcall():
    assert pytest.approx(Bondoptions(model,TO,TB,K).V_call(), abs=1e-6) == V_call

def test_Vput():
    assert pytest.approx(Bondoptions(model,TO,TB,K).V_put(), abs=1e-6) == V_put

