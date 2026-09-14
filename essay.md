# Where Wickham's Layered Grammar Departs from Wilkinson's Grammar of Graphics

The Wilkinson's original grammar defines the graphic generation as a series of
stages in order: DATA -> TRANS (data transition) -> Algebra (cross/nest/blend)
-> SCALE -> STAT/ELEMENT -> COORD (coordinate plane) -> Aesthetics mapping ->
GUIDE (labels etc.). And based on this Graphics Production Language (GPL) is
developed in Java.

Wickham later proposed "Layered Grammar of Graphics" defines the components of
a plot as: "a default dataset and set of mappings from variables to
aesthetics, one or more layers (each with geom + stat + position adjustment +
optional independent data/mapping), one scale for each aesthetic mapping used,
a coordinate system, the facet specification." The ideas presented in this
article have been implemented in the open-source R package, ggplot2.

There're some key differences between these two grammars:

## The treatment of statistics as layer components

Wickham's layer is equivalent to the Wilkinson's ELEMENT, but there's a key
difference in parameterization: In Wilkinson's grammar, all the parts of an
element are intertwined, while in Wickham's layered grammar they are separate.
For example, "The separation of statistic and geom enforced by the grammar
allows us to produce variations on the histogram. Using a ribbon instead of
bars produces a frequency polygon, and using points produces a graphic that
does not have its own name."

And the benefit of this design is that we can use same function and change the
parameters for the stat, and the combinations multiply without requiring
writing code for every single combination, the other benefit is that it makes
default layer possible, and it comes to another difference: defaults as a
design philosophy.

## Defaults as a design philosophy

Wilkinson's grammar insists "we cannot change the ordering of stages in the
pipeline... this is a truism", and this means explicit grammar that defines
every stage is always required.

But Wickham's layered grammar allows omit parts from the specification and
rely on defaults. We are able to omit parts from the specification and rely on
defaults. For example, if the stat is omitted, the geom will supply a default;
if the geom is omitted, the stat will supply a default.

And that buys the efficiency, users now save lots of time by the defaults and
don't always need explicit grammar.

## The handling of coordinates and faceting

In Wilkinson's grammar, faceting is an aspect of the coordinate system, but
the parameterization is kind of complicated: the faceting variable is
specified within the ELEMENT and a separate COORD specifies that the
coordinate system should be faceted by this variable.

In Wickham's layered grammar, this is less complicated, as the faceting is
independent of the layer and within-facet coordinate system.

This practice sacrifices flexibility, as the layout of the facets always
occurs in a Cartesian coordinate system, but reduces a lot in complexity.

## What these departures buy

Taken together, these departures buy composability and ease of use: by
separating stat from geom and letting layers, scales, and facets be specified
independently, Wickham's grammar lets users generate many valid chart
variations from the same small set of components, which helped drive
ggplot2's wide adoption. What is sacrificed is some of Wilkinson's formal
completeness, the guarantee that every stage of the pipeline is explicitly and
uniquely specified, along with the coordinate-system flexibility that let
faceting occur outside a fixed Cartesian layout.

## Grammar of graphics as the right abstraction level for AI chart generation

And there's a statement "a grammar of graphics is the right abstraction level
for AI chart generation — better than natural language above it or drawing
commands below it."

I think the statement is correct. A grammar of graphics is better than
natural language for AI chart generation has an inherent tolerance for
ambiguity. Natural language offers more flexibility of expression, but that
same flexibility introduces uncertainty for chart generation. Human expression
usually describes an image in the speaker's head, but it lacks rules, so it is
easy to leave out details that make the chart clear and unambiguous to an AI.
A grammar of graphics forces every parameter to be chosen explicitly. This
standardizes the expression, makes the chart specification valid, and removes
ambiguity. A grammar of graphics also keeps this meaning because it defines
data, stat, geom, and coordinate system as separate components. This means
switching a bar chart to a pie chart is just switching the coordinate system,
while the data and the statistical transformation stay the same. Drawing
commands do not have this structure. To turn the same data into a pie chart,
an AI has to calculate a completely different set of angles and arc paths from
scratch, instead of reusing the bar chart's logic. This makes errors more
likely and harder to catch.
