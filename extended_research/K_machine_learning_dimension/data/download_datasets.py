#!/usr/bin/env python3
"""
下载MNIST和CIFAR-10数据集
使用HTTP代理友好的方式
"""
import os
import urllib.request
import gzip
import pickle
import numpy as np

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def download_mnist():
    """下载MNIST数据集"""
    print("Downloading MNIST dataset...")
    
    base_url = "https://storage.googleapis.com/cvdf-datasets/mnist/"
    files = {
        'train_images': 'train-images-idx3-ubyte.gz',
        'train_labels': 'train-labels-idx1-ubyte.gz',
        'test_images': 't10k-images-idx3-ubyte.gz',
        'test_labels': 't10k-labels-idx1-ubyte.gz'
    }
    
    mnist_dir = os.path.join(DATA_DIR, 'mnist')
    os.makedirs(mnist_dir, exist_ok=True)
    
    for name, filename in files.items():
        filepath = os.path.join(mnist_dir, filename)
        if not os.path.exists(filepath):
            print(f"  Downloading {filename}...")
            try:
                urllib.request.urlretrieve(base_url + filename, filepath)
                print(f"    ✓ Saved to {filepath}")
            except Exception as e:
                print(f"    ✗ Failed: {e}")
                return False
        else:
            print(f"  ✓ {filename} already exists")
    
    return True

def download_cifar10():
    """下载CIFAR-10数据集"""
    print("\nDownloading CIFAR-10 dataset...")
    
    base_url = "https://www.cs.toronto.edu/~kriz/"
    filename = "cifar-10-python.tar.gz"
    
    cifar_dir = os.path.join(DATA_DIR, 'cifar10')
    os.makedirs(cifar_dir, exist_ok=True)
    
    filepath = os.path.join(cifar_dir, filename)
    if not os.path.exists(filepath):
        print(f"  Downloading {filename}...")
        try:
            urllib.request.urlretrieve(base_url + filename, filepath)
            print(f"    ✓ Saved to {filepath}")
            
            # 解压
            import tarfile
            print("  Extracting...")
            with tarfile.open(filepath, 'r:gz') as tar:
                tar.extractall(cifarDir)
            print("    ✓ Extracted")
        except Exception as e:
            print(f"    ✗ Failed: {e}")
            return False
    else:
        print(f"  ✓ {filename} already exists")
    
    return True

def generate_synthetic_mnist():
    """生成合成MNIST-like数据（当下载失败时使用）"""
    print("\nGenerating synthetic MNIST-like dataset...")
    
    np.random.seed(42)
    mnist_dir = os.path.join(DATA_DIR, 'mnist_synthetic')
    os.makedirs(mnist_dir, exist_ok=True)
    
    # 生成数据
    n_train = 60000
    n_test = 10000
    
    X_train = np.random.randn(n_train, 784).astype(np.float32) * 0.5
    y_train = np.random.randint(0, 10, n_train).astype(np.int64)
    
    X_test = np.random.randn(n_test, 784).astype(np.float32) * 0.5
    y_test = np.random.randint(0, 10, n_test).astype(np.int64)
    
    # 添加类特定模式
    for i in range(n_train):
        label = y_train[i]
        X_train[i, label*10:(label+1)*10] += np.random.randn(10) * 2
    
    for i in range(n_test):
        label = y_test[i]
        X_test[i, label*10:(label+1)*10] += np.random.randn(10) * 2
    
    # 保存
    np.savez(os.path.join(mnist_dir, 'mnist_synthetic.npz'),
             X_train=X_train, y_train=y_train,
             X_test=X_test, y_test=y_test)
    
    print(f"  ✓ Generated: {n_train} train, {n_test} test samples")
    print(f"  ✓ Saved to {mnist_dir}/mnist_synthetic.npz")
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("Dataset Download Script")
    print("=" * 60)
    
    # 尝试下载真实数据
    mnist_ok = download_mnist()
    cifar_ok = download_cifar10()
    
    # 如果下载失败，生成合成数据
    if not mnist_ok:
        print("\n⚠ MNIST download failed, generating synthetic data...")
        generate_synthetic_mnist()
    
    print("\n" + "=" * 60)
    print("Dataset preparation complete!")
    print("=" * 60)
