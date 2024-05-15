/** -*-c++-*-
 *
 *  Copyright 2015 The Australian National University
 *
 *  PersistencePairs.cpp
 *
 *  Reads a gradient vector field and computes persistence pairs.
 *
 *  Olaf Delgado-Friedrichs jun 15
 *
 *  Modified by Andrey Zubov, 30.04.2024
 *
 */
#ifndef PERSPEIREXTRACTOR_HPP
#define PERSPEIREXTRACTOR_HPP

#include <fstream>
#include <iterator>
// #include <chrono>

#include "chainComplexExtraction.hpp"
#include "CubicalComplex.hpp"
#include "SEDT.hpp"
#include "MorseVectorField.hpp"
#include "PackedMap.hpp"
#include "persistence.hpp"
#include "SimpleComplex.hpp"
#include "traversals.hpp"
#include "vectorFieldExtraction.hpp"
#include "VertexMap.hpp"

using namespace anu_am::diamorse;

typedef CubicalComplex::cell_id_type Cell;
typedef float Value;
typedef int8_t PhaseValue;
typedef VertexMap<CubicalComplex, Value> Scalars;
typedef MorseVectorField<PackedMap> Field;
typedef std::vector<std::pair<Cell, int>> Boundary;
typedef std::shared_ptr<std::vector<PhaseValue>> PhaseData;
typedef VertexMap<CubicalComplex, PhaseValue> Phases;

Value cellValue(Cell const v, Scalars const scalars, Vertices const vertices)
{
    Value val = scalars.get(vertices(v, 0));
    for (size_t i = 1; i < (size_t)vertices.count(v); ++i)
        val = std::max(val, scalars.get(vertices(v, i)));

    return val;
}

struct Comparator
{
    Comparator(CubicalComplex const &complex, Scalars const &scalars)
        : _complex(complex),
          _vertices(complex.xdim(), complex.ydim(), complex.zdim()),
          _scalars(scalars)
    {
    }

    bool operator()(Cell const v, Cell const w)
    {
        Value const sv = cellValue(v, _scalars, _vertices);
        Value const sw = cellValue(w, _scalars, _vertices);

        return sv < sw or
               (sv == sw &&
                _complex.cellDimension(v) < _complex.cellDimension(w));
    }

private:
    CubicalComplex const &_complex;
    Vertices const _vertices;
    Scalars const &_scalars;
};

std::vector<Cell> criticalCellsSorted(
    CubicalComplex const &complex,
    Scalars const &scalars,
    Field const &field)
{
    std::vector<Cell> critical;

    for (Cell cell = 0; cell <= complex.cellIdLimit(); ++cell)
        if (complex.isCell(cell) && field.isCritical(cell))
            critical.push_back(cell);

    std::stable_sort(critical.begin(), critical.end(),
                     Comparator(complex, scalars));

    return critical;
}

SimpleComplex simpleChainComplex(
    CubicalComplex const &complex,
    Scalars const &scalars,
    std::map<Cell, Boundary> const &chains,
    std::vector<Cell> const &sources)
{
    size_t const n = sources.size();
    Vertices const vertices(complex.xdim(), complex.ydim(), complex.zdim());

    std::map<Cell, size_t> index;
    for (size_t i = 0; i < n; ++i)
        index[sources.at(i)] = i;

    std::vector<unsigned int> dims;
    std::vector<float> values;
    std::vector<std::vector<Cell>> faceLists;

    for (size_t i = 0; i < n; ++i)
    {
        Cell const v = sources.at(i);
        dims.push_back(complex.cellDimension(v));
        values.push_back(cellValue(v, scalars, vertices));

        Boundary const flin = chains.at(v);
        std::vector<Cell> flout;
        for (size_t j = 0; j < flin.size(); ++j)
        {
            std::pair<Cell, int> p = flin.at(j);
            for (int k = 0; k < p.second; ++k)
                flout.push_back(index.at(p.first));
        }

        faceLists.push_back(flout);
    }

    return SimpleComplex(dims, values, faceLists);
}

Phases computePhases(
    PhaseData &image_data,
    CubicalComplex const &complex)
{
    auto phase_data = std::make_shared<std::vector<std::int8_t>>();
    phase_data->swap(*image_data);
    Phases phases(complex, phase_data);
    return phases;
}

Scalars computeScalars(
    PhaseData &image_data,
    CubicalComplex const &complex)
{
    const Phases phases = computePhases(image_data, complex);
    Scalars scalars(complex);
    classify(complex, phases, scalars);
    compute(complex, scalars);
    return scalars;
}

Field computeVectorField(
    CubicalComplex const &complex,
    Scalars const &scalar)
{
    Field field(complex);
    fillMorseVectorField(complex, scalar, field);
    return field;
}

struct Triplet
{
    std::int32_t x;
    std::int32_t y;
    std::int32_t z;
};

struct Result
{
    std::vector<std::pair<float, float>> pd0;
    std::vector<std::pair<float, float>> pd1;
    std::vector<std::pair<float, float>> pd2;
};

class PersPairExtractor
{
public:
    static Result extract(std::vector<PhaseValue> data, Triplet size)
    {
        auto ptr_data = std::make_shared<std::vector<PhaseValue>>(std::move(data));

        auto complex = std::make_shared<CubicalComplex>(size.x, size.y, size.z);
        Vertices vertices(size.x, size.y, size.z);

        auto scalars = computeScalars(ptr_data, *complex);
        auto field = computeVectorField(*complex, scalars);

        // Process the data.
        const std::map<Cell, Boundary> chains =
            chainComplex(*complex, field);

        std::vector<Cell> const sources =
            criticalCellsSorted(*complex, scalars, field);

        SimpleComplex const simple =
            simpleChainComplex(*complex, scalars, chains, sources);

        std::vector<Pairing<Cell>> const pairs =
            persistencePairing(simple);

        std::vector<std::pair<float, float>> pd0;
        std::vector<std::pair<float, float>> pd1;
        std::vector<std::pair<float, float>> pd2;

        for (auto i = 0; i < pairs.size(); ++i)
        {
            auto j = pairs.at(i).partner;
            if (pairs.at(i).dimension == 3 || j >= pairs.size())
            {
                continue;
            }
            Cell const v = sources.at(i);
            Cell const w = sources.at(j);
            if (v != w)
            {
                if (pairs.at(i).dimension == 0 && pairs.at(j).dimension == 1)
                {
                    pd0.push_back(std::make_pair(cellValue(v, scalars, vertices),
                                                 cellValue(w, scalars, vertices)));
                }
                if (pairs.at(i).dimension == 1 && pairs.at(j).dimension == 2)
                {
                    pd1.push_back(std::make_pair(cellValue(v, scalars, vertices),
                                                 cellValue(w, scalars, vertices)));
                }
                if (pairs.at(i).dimension == 2 && pairs.at(j).dimension == 3)
                {
                    pd2.push_back(std::make_pair(cellValue(v, scalars, vertices),
                                                 cellValue(w, scalars, vertices)));
                }
            }
        }
        return {pd0, pd1, pd2};
    }
};
#endif // PERSPEIREXTRACTOR_HPP