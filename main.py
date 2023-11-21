import graphviz
import math
import os
import matplotlib.pyplot as plt
from matplotlib.image import imread

ID = 1

main_view_fig, main_view_ax = plt.subplots()
main_view_ax.axis("off")

auxiliary_fig, auxiliary_axs = plt.subplots(1, 3, figsize=(12, 4))
for ax in auxiliary_axs:
    ax.axis('off')

text_fig, text_ax = plt.subplots(figsize=(6, 20))
with open("code.txt", "r") as f:
    code = f.read()
text_ax.text(0, -0.1, code, fontsize=12, color='black')
text_ax.axis('off')

log_fig, log_ax = plt.subplots()
log_ax.axis('off')
log_ax.set_title("Logs")
logs = ""
state="Current state\n1. grand doesn't exist\n2. tmp doesn't exist\n3. oldTmp doesn't exist\n4. count doesn't exist\n\
5. m doesn't exist\n6. h doesn't exist\n7. m (in for loop) doesn't exist"

class StateParams:
    GRAND = "1. "
    TMP = "2. "
    OLDTMP = "3. "
    COUNT = "4. "
    M = "5. "
    H = "6. "
    M_LOOP = "7. "

def update_state(param: str, new_row: str):
    global state
    lines = state.split('\n')
    modified_lines = []
    for line in lines:
        if param in line:
            modified_lines.append(new_row)
        else:
            modified_lines.append(line)
    state = '\n'.join(modified_lines)


def update_logs():
    plt.figure(log_fig.number)

    log_ax.clear()
    log_ax.axis('off')
    log_ax.set_title("Logs")

    log_ax.text(0.6, 0.6, state, fontsize=10, color='black')

    log_ax.text(0, 0, logs, fontsize=12, color='black')
    plt.waitforbuttonpress()
    plt.pause(0.00001)


def visualize_binary_tree(root, axname=None):
    global ID, logs
    dot_preorder = graphviz.Digraph(comment='Preorder Traversal')
    BST.preorder_traversal(root, dot_preorder)
    dot_preorder.render('preorder_traversal', format='png',
                        outfile=f'images/preorder_traversal{ID}.png')
    impath = f"images/preorder_traversal{ID}.png"
    plt.figure(main_view_fig.number)
    main_view_ax.set_title(axname)
    main_view_ax.imshow(imread(impath))
    plt.waitforbuttonpress()
    plt.pause(0.00001)
    ID += 1

    # plt.figure(auxiliary_fig.number)
    for i in range(3):
        auxiliary_axs[i].clear()
        auxiliary_axs[i].axis('off')
    plt.waitforbuttonpress()
    plt.pause(0.00001)

    logs = ""
    update_logs()


def visualize_auxiliary_trees(parent: int, child: int, subplot: int, ax_title: str):
    global ID
    ax = auxiliary_axs[subplot]
    dot_auxiliary = graphviz.Digraph(comment=f'auxiliary {subplot}')
    dot_auxiliary.node(str(parent), label=str(parent))
    dot_auxiliary.node(str(child), label=str(child))
    dot_auxiliary.edge(str(parent), str(child), style='filled')

    impath = f"images/auxiliary{ID}.png"
    dot_auxiliary.render("auxiliary", format='png',
                         outfile=impath)
    plt.figure(auxiliary_fig.number)
    ax.set_title(ax_title)
    ax.imshow(imread(impath))
    plt.waitforbuttonpress()
    plt.pause(0.00001)

    ID += 1


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


GRAND = TreeNode("auxiliary node")


class BST:
    def __init__(self):
        self.root = None

    def insert(self, val):
        if self.root is None:
            self.root = TreeNode(val)
        else:
            self._insert(self.root, val)

    def _insert(self, node, val):
        if val > node.val:
            if node.right:
                self._insert(node.right, val)
            else:
                node.right = TreeNode(val)
        elif val < node.val:
            if node.left:
                self._insert(node.left, val)
            else:
                node.left = TreeNode(val)

    def bstToVine(self, grand: TreeNode) -> int:
        global logs
        count = 0
        update_state(StateParams.COUNT, StateParams.COUNT + f"count is {count}")
        logs += f"3. tmp = grand.right -> tmp is TreeNode({grand.right.val})\n"
        update_logs()
        tmp = grand.right
        update_state(StateParams.TMP, StateParams.TMP + f"tmp is {tmp and f'TreeNode({tmp.val})'}")
        while tmp:
            if tmp.left:

                if tmp:
                    logs += f"6. oldTmp = tmp -> oldTmp is TreeNode({tmp.val})\n"
                else:
                    logs += f"6. oldTmp = tmp -> oldTmp is None\n"
                oldTmp = tmp
                update_state(StateParams.OLDTMP, StateParams.OLDTMP + f"oldTmp is {oldTmp and f'TreeNode({oldTmp.val})'}")
                update_logs()
                if tmp.left:
                    logs += f"7. tmp = tmp.left -> tmp is TreeNode({tmp.left.val})\n"
                else:
                    logs += f"7. tmp = tmp.left -> tmp is None\n"
                tmp = tmp.left
                update_state(StateParams.TMP, StateParams.TMP + f"tmp is {tmp and f'TreeNode({tmp.val})'}")
                update_logs()
                oldTmp.left = tmp.right
                if tmp.right is None:
                    visualize_auxiliary_trees(oldTmp.val, None, 0, f"8. oldTmp.left = tmp.right")
                else:
                    visualize_auxiliary_trees(oldTmp.val, tmp.right.val, 0, f"8. oldTmp.left = tmp.right")
                tmp.right = oldTmp
                if oldTmp is None:
                    visualize_auxiliary_trees(tmp.val, None, 1, f"9. tmp.right = oldTmp")
                else:
                    visualize_auxiliary_trees(tmp.val, oldTmp.val, 1, f"9. tmp.right = oldTmp")
                grand.right = tmp
                if tmp is None:
                    visualize_auxiliary_trees(grand.val, None, 2, f"10. grand.right = tmp")
                else:
                    visualize_auxiliary_trees(grand.val, tmp.val, 2, f"10. grand.right = tmp")

                visualize_binary_tree(GRAND, "Turning tree into vine")

            else:
                logs = ""
                update_logs()
                count += 1
                logs += f"12. count += 1 -> count is {count}\n"
                update_state(StateParams.COUNT, StateParams.COUNT + f"count is {count}")
                update_logs()
                if tmp:
                    logs += f"13. grand = tmp -> grand is TreeNode({tmp.val})\n"
                else:
                    logs += "13. grand = tmp -> grand is None\n"
                update_logs()
                grand = tmp
                update_state(StateParams.GRAND, StateParams.GRAND + f"grand is {grand and f'TreeNode({grand.val})'}")
                if tmp.right:
                    logs += f"14. tmp = tmp.right -> tmp is TreeNode({tmp.right.val})\n"
                else:
                    logs += "14. tmp = tmp.right -> tmp is None\n"
                update_logs()
                tmp = tmp.right
                update_state(StateParams.TMP, StateParams.TMP + f"tmp is {tmp and f'TreeNode({tmp.val})'}")
                update_logs()
        return count

    def compress(self, grand: TreeNode, m: int) -> None:
        global logs
        if grand.right:
            logs += f"18. tmp = grand.right -> tmp is TreeNode({grand.right.val})\n"
        else:
            logs += "18. tmp = grand.right -> tmp is None\n"
        tmp = grand.right
        update_state(StateParams.TMP, StateParams.TMP + f"tmp is {tmp and f'TreeNode({tmp.val})'}")
        update_logs()
        for _ in range(m):
            if tmp:
                logs += f"20. oldTmp = tmp -> oldTmp is TreeNode({tmp.val})\n"
            else:
                logs += "20. oldTmp = tmp -> oldTmp is None\n"
            oldTmp = tmp
            update_state(StateParams.OLDTMP, StateParams.OLDTMP + f"oldTmp is {oldTmp and f'TreeNode({oldTmp.val})'}")
            update_logs()
            if tmp.right:
                logs += f"21. tmp = tmp.right -> tmp is TreeNode({tmp.right.val})\n"
            else:
                logs += "21. tmp = tmp.right -> tmp is None\n"
            tmp = tmp.right
            update_state(StateParams.TMP, StateParams.TMP + f"tmp is {tmp and f'TreeNode({tmp.val})'}")
            update_logs()
            grand.right = tmp
            if tmp is None:
                visualize_auxiliary_trees(grand.val, None, 0, "22. grand.right = tmp")
            else:
                visualize_auxiliary_trees(grand.val, tmp.val, 0, "22. grand.right = tmp")

            oldTmp.right = tmp.left
            if tmp.left is None:
                visualize_auxiliary_trees(oldTmp.val, None, 1, "23. oldTmp.right = tmp.left")
            else:
                visualize_auxiliary_trees(oldTmp.val, tmp.left.val, 1, "23. oldTmp.right = tmp.left")

            tmp.left = oldTmp
            if oldTmp is None:
                visualize_auxiliary_trees(tmp.val, None, 2, "24. tmp.left = oldTmp")
            else:
                visualize_auxiliary_trees(tmp.val, oldTmp.val, 2, "24. tmp.left = oldTmp")

            grand = tmp
            update_state(StateParams.GRAND, StateParams.GRAND + f"grand is {grand and f'TreeNode({grand.val})'}")
            if tmp:
                logs += f"25. grand = tmp -> grand is TreeNode({tmp.val})\n"
            else:
                logs += "25. grand = tmp -> grand is None\n"
            update_logs()
            tmp = tmp.right
            update_state(StateParams.TMP, StateParams.TMP + f"tmp is {tmp and f'TreeNode({tmp.val})'}")
            if tmp.right:
                logs += f"26. tmp = tmp.right -> tmp is TreeNode({tmp.right.val})\n"
            else:
                logs += "26. tmp = tmp.right -> tmp is None\n"
            update_logs()
            visualize_binary_tree(GRAND, "Compression")

    def balanceBST(self, root: TreeNode) -> TreeNode:
        global logs
        GRAND.right = root
        visualize_binary_tree(root, "Original tree")  # or root instead of GRAND
        count = self.bstToVine(GRAND)
        h = int(math.log2(count + 1))
        update_state(StateParams.H, StateParams.H + f"h is {h}")
        logs += f"h = int(math.log2(count + 1)) -> h is {int(math.log2(count + 1))}\n"
        update_logs()
        m = pow(2, h) - 1
        update_state(StateParams.M, StateParams.M + f"m is {m}")
        logs += f"m = pow(2, h) - 1 -> m is {pow(2, h) - 1}\n"
        update_logs()
        self.compress(GRAND, count - m)
        for m in [m // 2**i for i in range(1, h + 1)]:
            update_state(StateParams.M_LOOP, StateParams.M_LOOP + f"m (in for loop) is {m}")
            self.compress(GRAND, m)

        self.root = GRAND.right
        logs += f"self.root = GRAND.right -> self.root is TreeNode({GRAND.right.val})\n"
        visualize_binary_tree(self.root, "Result of balancing")
        return GRAND.right

    @staticmethod
    def preorder_traversal(root, dot):
        if root:
            dot.node(str(root.val), label=str(root.val))
            if root.left:
                dot.edge(str(root.val), str(root.left.val), style='filled')
            if root.right:
                dot.edge(str(root.val), str(root.right.val), style='filled')
            BST.preorder_traversal(root.left, dot)
            BST.preorder_traversal(root.right, dot)


os.makedirs("images", exist_ok=True)

bst = BST()
elements = [5, 4, 6, 3, 10, 9, 8]
for e in elements:
    bst.insert(e)
bst.balanceBST(bst.root)

plt.show()
