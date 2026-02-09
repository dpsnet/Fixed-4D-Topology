#!/bin/bash
# 批量编译所有论文为PDF

set -e

echo "========================================="
echo "  批量编译所有论文为PDF"
echo "========================================="

# 定义论文列表
PAPERS=(
    "./arxiv-paper/main.tex:arxiv-paper/main.pdf"
    "./docs/Dimensionics-Physics/paper/Dimensionics_Physics.tex:docs/Dimensionics-Physics/paper/Dimensionics_Physics.pdf"
    "./docs/Dimensionics-Physics/paper/COVER_LETTER.tex:docs/Dimensionics-Physics/paper/COVER_LETTER.pdf"
    "./papers/unified-dimensionics/latex/main.tex:papers/unified-dimensionics/latex/main.pdf"
    "./extended_research/K_machine_learning_dimension/paper/neurips_submission/main.tex:extended_research/K_machine_learning_dimension/paper/neurips_submission/main.pdf"
    "./extended_research/K_machine_learning_dimension/paper/neurips_submission/supplementary_materials.tex:extended_research/K_machine_learning_dimension/paper/neurips_submission/supplementary_materials.pdf"
)

COMPILE_DIR=$(pwd)
COMPILED=0
FAILED=0

for item in "${PAPERS[@]}"; do
    texfile="${item%%:*}"
    pdffile="${item##*:}"
    
    if [ ! -f "$texfile" ]; then
        echo "⚠️  跳过: $texfile (文件不存在)"
        continue
    fi
    
    echo ""
    echo "📄 编译: $texfile"
    echo "----------------------------------------"
    
    dir=$(dirname "$texfile")
    base=$(basename "$texfile" .tex)
    
    cd "$dir" || continue
    
    # 编译LaTeX
    if pdflatex -interaction=nonstopmode -halt-on-error "${base}.tex" > /dev/null 2>&1; then
        if pdflatex -interaction=nonstopmode -halt-on-error "${base}.tex" > /dev/null 2>&1; then
            if [ -f "${base}.pdf" ]; then
                mv "${base}.pdf" "$COMPILE_DIR/$pdffile" 2>/dev/null || true
                echo "   ✅ 成功: $pdffile"
                ((COMPILED++))
            else
                echo "   ❌ 失败: PDF未生成"
                ((FAILED++))
            fi
        else
            echo "   ⚠️  警告: 第二次编译失败"
            if [ -f "${base}.pdf" ]; then
                mv "${base}.pdf" "$COMPILE_DIR/$pdffile" 2>/dev/null || true
                echo "   ✅ 部分成功: $pdffile"
                ((COMPILED++))
            else
                ((FAILED++))
            fi
        fi
    else
        echo "   ❌ 失败: 编译错误"
        ((FAILED++))
    fi
    
    # 清理辅助文件
    rm -f "${base}.aux" "${base}.log" "${base}.out" "${base}.toc" "${base}.bbl" "${base}.blg"
    
    cd "$COMPILE_DIR" || exit 1
done

echo ""
echo "========================================="
echo "  编译完成: $COMPILED 成功, $FAILED 失败"
echo "========================================="
