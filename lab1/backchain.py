from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    # print ("backchain_to_goal_tree", rules, hypothesis)
    result = OR(hypothesis)

    for rule in rules:
        for then in rule.consequent():
            m = match(then, hypothesis)
            if m == None:
                continue

            if isinstance (rule.antecedent(), AND):
                new_rule = AND([backchain_to_goal_tree(rules, populate(pattern, m)) for pattern in rule.antecedent()])
                result.append(new_rule)
            elif isinstance (rule.antecedent(), OR):
                new_rule = OR([backchain_to_goal_tree(rules, populate(pattern, m)) for pattern in rule.antecedent()])
                result.append(new_rule)
            elif isinstance (rule.antecedent(), str):
                new_rule = OR(backchain_to_goal_tree(rules, populate(rule.antecedent(), m)))
                result.extend(new_rule)
            else:
                print("backchain_to_goal_tree confusing antecedent", rule.antecedent)
                return None

    return simplify(result)

# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
