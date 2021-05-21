class TreeNode:
    def __init__(self, x):
        self.val = x
        self.parent = None
        self.left = None
        self.right = None

    def emerge(self):
        if self.left.val == self.right.val:
            self.val = self.left.val
            self.left = None
            self.right = None
