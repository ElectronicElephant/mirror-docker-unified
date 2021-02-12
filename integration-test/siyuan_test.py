import requests

BASE_URL = "mirror.sjtu.edu.cn"

"""
Here we take Debian repo as an example. It should be served on both http
and https. Caddy should handle the redirections correctly.
"""

def test_debian_http_base():
    response = requests.get(f"http://{BASE_URL}/debian")
    assert response.history
    assert response.url == f"http://{BASE_URL}/debian/"

def test_debian_http_dir():
    response = requests.get(f"http://{BASE_URL}/debian/pool")
    assert response.history
    assert response.url == f"http://{BASE_URL}/debian/pool/"

def test_debian_https_base():
    response = requests.get(f"https://{BASE_URL}/debian")
    assert response.history
    assert response.url == f"https://{BASE_URL}/debian/"

def test_debian_https_dir():
    response = requests.get(f"https://{BASE_URL}/debian/pool")
    assert response.history
    assert response.url == f"https://{BASE_URL}/debian/pool/"

"""
Here we take conda repo as an example. It should be served only on https
interface. All http request should be redirected to https.
"""

""" Currently Siyuan mirror has no such entry.

def test_conda_http_base():
    response = requests.get(f"http://{BASE_URL}/anaconda")
    assert response.history
    assert response.url == f"https://{BASE_URL}/anaconda/"

def test_conda_http_dir():
    response = requests.get(f"http://{BASE_URL}/anaconda/cloud")
    assert response.history
    assert response.url == f"https://{BASE_URL}/anaconda/cloud/"

def test_conda_https_base():
    response = requests.get(f"https://{BASE_URL}/anaconda")
    assert response.history
    assert response.url == f"https://{BASE_URL}/anaconda/"

def test_conda_https_dir():
    response = requests.get(f"https://{BASE_URL}/anaconda/cloud")
    assert response.history
    assert response.url == f"https://{BASE_URL}/anaconda/cloud/"

def test_conda_file():
    response = requests.get(f"http://{BASE_URL}/anaconda/cloud/pytorch/noarch/repodata.json")
    assert response.history
    assert response.url == f"https://{BASE_URL}/anaconda/cloud/pytorch/noarch/repodata.json"
"""

"""
And for our frontend, it should always be available on https.
"""

def test_frontend_base():
    response = requests.get(f"http://{BASE_URL}")
    assert response.history
    assert response.url == f"https://{BASE_URL}/"

def test_frontend_docs():
    response = requests.get(f"http://{BASE_URL}/docs/anaconda")
    assert response.history
    assert response.status_code == 200
    assert response.url == f"https://{BASE_URL}/docs/anaconda"

def test_lug_base():
    response = requests.get(f"http://{BASE_URL}/lug/v1/manager/summary")
    assert response.history
    assert response.url == f"https://{BASE_URL}/lug/v1/manager/summary"

"""
Also an edge case, we should never concat two directories
"""

def test_debian_concat():
    response = requests.get(f"http://{BASE_URL}/debiandoc/source-unpack.txt")
    assert response.status_code == 404

"""
For git repos, should redirect to git.sjtu
"""

def test_git_redirect():
    response = requests.get(f"http://{BASE_URL}/git/llvm-project.git")
    assert response.url == f"https://git.sjtu.edu.cn/sjtug/llvm-project"

"""
We should return x-sjtug-mirror-id in header
"""
def test_mirror_id():
    response = requests.get(f"http://{BASE_URL}")
    assert response.headers["x-sjtug-mirror-id"] == "siyuan"
