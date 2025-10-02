#!/usr/bin/env python3
"""
Demo script to show how the utils functions work
"""
from utils import access_nested_map, get_json, memoize
from client import GithubOrgClient


def demo_access_nested_map():
    """Demonstrate access_nested_map function"""
    print("=== Demonstrating access_nested_map ===")
    
    # Example 1: Simple nested map
    nested_map = {"a": 1}
    path = ("a",)
    result = access_nested_map(nested_map, path)
    print(f"access_nested_map({nested_map}, {path}) = {result}")
    
    # Example 2: Deeper nesting
    nested_map = {"a": {"b": 2}}
    path = ("a", "b")
    result = access_nested_map(nested_map, path)
    print(f"access_nested_map({nested_map}, {path}) = {result}")
    
    # Example 3: KeyError case
    try:
        nested_map = {}
        path = ("a",)
        result = access_nested_map(nested_map, path)
    except KeyError as e:
        print(f"access_nested_map({nested_map}, {path}) raises KeyError: {e}")
    
    print()


def demo_memoize():
    """Demonstrate memoize decorator"""
    print("=== Demonstrating memoize decorator ===")
    
    class TestClass:
        def __init__(self):
            self.call_count = 0

        def expensive_method(self):
            self.call_count += 1
            print(f"expensive_method called! (call #{self.call_count})")
            return 42

        @memoize
        def cached_property(self):
            return self.expensive_method()

    obj = TestClass()
    
    print("First access to cached_property:")
    result1 = obj.cached_property
    print(f"Result: {result1}")
    
    print("Second access to cached_property:")
    result2 = obj.cached_property
    print(f"Result: {result2}")
    
    print(f"Total calls to expensive_method: {obj.call_count}")
    print()


def demo_github_client():
    """Demonstrate GithubOrgClient (without making actual API calls)"""
    print("=== Demonstrating GithubOrgClient ===")
    
    # Create client instance
    client = GithubOrgClient("google")
    
    # Show the URL that would be used
    print(f"GitHub API URL for 'google' org: {client.ORG_URL.format(org='google')}")
    
    # Demonstrate has_license method
    repo_with_license = {
        "license": {"key": "apache-2.0"}
    }
    
    repo_without_license = {}
    
    print(f"Repo with Apache 2.0 license: {client.has_license(repo_with_license, 'apache-2.0')}")
    print(f"Repo with Apache 2.0 license (checking for MIT): {client.has_license(repo_with_license, 'mit')}")
    print(f"Repo without license: {client.has_license(repo_without_license, 'apache-2.0')}")
    
    print()


if __name__ == "__main__":
    print("🧪 Utils and Client Demo\n")
    demo_access_nested_map()
    demo_memoize()
    demo_github_client()
    print("✅ Demo completed!")