/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Rewriters                                                                  *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|* From: VhloToVersionPatterns.td                                             *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

/* Generated from:
    external/stablehlo/stablehlo/transforms/VhloToVersionPatterns.td:25
*/
struct DynamicConvDowngradeV2ToV1 : public ::mlir::RewritePattern {
  DynamicConvDowngradeV2ToV1(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("vhlo.dynamic_conv_v2", 1, context, {"vhlo.dynamic_conv_v1"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Attribute feature_group_count;
    ::mlir::Attribute output_feature_dimension;
    ::mlir::Operation::operand_range lhs(op0->getOperands());
    ::mlir::Operation::operand_range rhs(op0->getOperands());
    ::mlir::Attribute output_batch_dimension;
    ::mlir::Attribute lhs_dilation;
    ::mlir::Attribute output_spatial_dimensions;
    ::mlir::Attribute window_reversal;
    ::mlir::Operation::operand_range d_padding(op0->getOperands());
    ::mlir::Attribute rhs_dilation;
    ::mlir::Attribute input_batch_dimension;
    ::mlir::Attribute window_strides;
    ::mlir::Attribute input_spatial_dimensions;
    ::mlir::Attribute kernel_spatial_dimensions;
    ::mlir::Attribute precision_config;
    ::mlir::Attribute batch_group_count;
    ::mlir::Attribute input_feature_dimension;
    ::mlir::Attribute kernel_input_feature_dimension;
    ::mlir::Attribute kernel_output_feature_dimension;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::vhlo::DynamicConvOpV2>(op0); (void)castedOp0;
    lhs = castedOp0.getODSOperands(0);
    rhs = castedOp0.getODSOperands(1);
    d_padding = castedOp0.getODSOperands(2);
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("window_strides");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v2' to have attribute 'window_strides' of type '::mlir::Attribute'";
        });
      }
      window_strides = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("lhs_dilation");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v2' to have attribute 'lhs_dilation' of type '::mlir::Attribute'";
        });
      }
      lhs_dilation = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("rhs_dilation");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v2' to have attribute 'rhs_dilation' of type '::mlir::Attribute'";
        });
      }
      rhs_dilation = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("window_reversal");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v2' to have attribute 'window_reversal' of type '::mlir::Attribute'";
        });
      }
      window_reversal = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("input_batch_dimension");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v2' to have attribute 'input_batch_dimension' of type '::mlir::Attribute'";
        });
      }
      input_batch_dimension = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("input_feature_dimension");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v2' to have attribute 'input_feature_dimension' of type '::mlir::Attribute'";
        });
      }
      input_feature_dimension = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("input_spatial_dimensions");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v2' to have attribute 'input_spatial_dimensions' of type '::mlir::Attribute'";
        });
      }
      input_spatial_dimensions = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("kernel_input_feature_dimension");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v2' to have attribute 'kernel_input_feature_dimension' of type '::mlir::Attribute'";
        });
      }
      kernel_input_feature_dimension = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("kernel_output_feature_dimension");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v2' to have attribute 'kernel_output_feature_dimension' of type '::mlir::Attribute'";
        });
      }
      kernel_output_feature_dimension = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("kernel_spatial_dimensions");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v2' to have attribute 'kernel_spatial_dimensions' of type '::mlir::Attribute'";
        });
      }
      kernel_spatial_dimensions = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("output_batch_dimension");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v2' to have attribute 'output_batch_dimension' of type '::mlir::Attribute'";
        });
      }
      output_batch_dimension = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("output_feature_dimension");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v2' to have attribute 'output_feature_dimension' of type '::mlir::Attribute'";
        });
      }
      output_feature_dimension = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("output_spatial_dimensions");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v2' to have attribute 'output_spatial_dimensions' of type '::mlir::Attribute'";
        });
      }
      output_spatial_dimensions = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("feature_group_count");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v2' to have attribute 'feature_group_count' of type '::mlir::Attribute'";
        });
      }
      feature_group_count = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("batch_group_count");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v2' to have attribute 'batch_group_count' of type '::mlir::Attribute'";
        });
      }
      batch_group_count = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("precision_config");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v2' to have attribute 'precision_config' of type '::mlir::Attribute'";
        });
      }
      precision_config = tblgen_attr;
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    auto nativeVar_0 = getDefaultConvPadding(rewriter, (*lhs.begin())); (void)nativeVar_0;
    ::mlir::vhlo::DynamicConvOpV1 tblgen_DynamicConvOpV1_1;
    {
      ::llvm::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::llvm::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*lhs.begin()));
      tblgen_values.push_back((*rhs.begin()));
      tblgen_values.push_back((*d_padding.begin()));
      if (auto tmpAttr = window_strides) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("window_strides"), tmpAttr);
      }
      if (auto tmpAttr = nativeVar_0) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("padding"), tmpAttr);
      }
      if (auto tmpAttr = lhs_dilation) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("lhs_dilation"), tmpAttr);
      }
      if (auto tmpAttr = rhs_dilation) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("rhs_dilation"), tmpAttr);
      }
      if (auto tmpAttr = window_reversal) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("window_reversal"), tmpAttr);
      }
      if (auto tmpAttr = input_batch_dimension) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("input_batch_dimension"), tmpAttr);
      }
      if (auto tmpAttr = input_feature_dimension) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("input_feature_dimension"), tmpAttr);
      }
      if (auto tmpAttr = input_spatial_dimensions) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("input_spatial_dimensions"), tmpAttr);
      }
      if (auto tmpAttr = kernel_input_feature_dimension) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("kernel_input_feature_dimension"), tmpAttr);
      }
      if (auto tmpAttr = kernel_output_feature_dimension) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("kernel_output_feature_dimension"), tmpAttr);
      }
      if (auto tmpAttr = kernel_spatial_dimensions) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("kernel_spatial_dimensions"), tmpAttr);
      }
      if (auto tmpAttr = output_batch_dimension) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("output_batch_dimension"), tmpAttr);
      }
      if (auto tmpAttr = output_feature_dimension) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("output_feature_dimension"), tmpAttr);
      }
      if (auto tmpAttr = output_spatial_dimensions) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("output_spatial_dimensions"), tmpAttr);
      }
      if (auto tmpAttr = feature_group_count) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("feature_group_count"), tmpAttr);
      }
      if (auto tmpAttr = batch_group_count) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("batch_group_count"), tmpAttr);
      }
      if (auto tmpAttr = precision_config) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("precision_config"), tmpAttr);
      }
      ::llvm::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_DynamicConvOpV1_1 = rewriter.create<::mlir::vhlo::DynamicConvOpV1>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_DynamicConvOpV1_1.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

/* Generated from:
    external/stablehlo/stablehlo/transforms/VhloToVersionPatterns.td:21
*/
struct DynamicConvUpgradeV1ToV2 : public ::mlir::RewritePattern {
  DynamicConvUpgradeV1ToV2(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("vhlo.dynamic_conv_v1", 1, context, {"vhlo.dynamic_conv_v2"}) {}
  ::mlir::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Attribute feature_group_count;
    ::mlir::Attribute output_feature_dimension;
    ::mlir::Attribute kernel_spatial_dimensions;
    ::mlir::Operation::operand_range lhs(op0->getOperands());
    ::mlir::Operation::operand_range rhs(op0->getOperands());
    ::mlir::Attribute output_batch_dimension;
    ::mlir::Attribute lhs_dilation;
    ::mlir::Attribute output_spatial_dimensions;
    ::mlir::Attribute window_reversal;
    ::mlir::Operation::operand_range d_padding(op0->getOperands());
    ::mlir::Attribute padding;
    ::mlir::Attribute rhs_dilation;
    ::mlir::Attribute input_batch_dimension;
    ::mlir::Attribute window_strides;
    ::mlir::Attribute input_spatial_dimensions;
    ::mlir::Attribute precision_config;
    ::mlir::Attribute batch_group_count;
    ::mlir::Attribute kernel_input_feature_dimension;
    ::mlir::Attribute input_feature_dimension;
    ::mlir::Attribute kernel_output_feature_dimension;
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::vhlo::DynamicConvOpV1>(op0); (void)castedOp0;
    lhs = castedOp0.getODSOperands(0);
    rhs = castedOp0.getODSOperands(1);
    d_padding = castedOp0.getODSOperands(2);
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("window_strides");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v1' to have attribute 'window_strides' of type '::mlir::Attribute'";
        });
      }
      window_strides = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("padding");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v1' to have attribute 'padding' of type '::mlir::Attribute'";
        });
      }
      padding = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("lhs_dilation");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v1' to have attribute 'lhs_dilation' of type '::mlir::Attribute'";
        });
      }
      lhs_dilation = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("rhs_dilation");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v1' to have attribute 'rhs_dilation' of type '::mlir::Attribute'";
        });
      }
      rhs_dilation = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("window_reversal");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v1' to have attribute 'window_reversal' of type '::mlir::Attribute'";
        });
      }
      window_reversal = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("input_batch_dimension");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v1' to have attribute 'input_batch_dimension' of type '::mlir::Attribute'";
        });
      }
      input_batch_dimension = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("input_feature_dimension");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v1' to have attribute 'input_feature_dimension' of type '::mlir::Attribute'";
        });
      }
      input_feature_dimension = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("input_spatial_dimensions");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v1' to have attribute 'input_spatial_dimensions' of type '::mlir::Attribute'";
        });
      }
      input_spatial_dimensions = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("kernel_input_feature_dimension");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v1' to have attribute 'kernel_input_feature_dimension' of type '::mlir::Attribute'";
        });
      }
      kernel_input_feature_dimension = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("kernel_output_feature_dimension");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v1' to have attribute 'kernel_output_feature_dimension' of type '::mlir::Attribute'";
        });
      }
      kernel_output_feature_dimension = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("kernel_spatial_dimensions");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v1' to have attribute 'kernel_spatial_dimensions' of type '::mlir::Attribute'";
        });
      }
      kernel_spatial_dimensions = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("output_batch_dimension");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v1' to have attribute 'output_batch_dimension' of type '::mlir::Attribute'";
        });
      }
      output_batch_dimension = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("output_feature_dimension");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v1' to have attribute 'output_feature_dimension' of type '::mlir::Attribute'";
        });
      }
      output_feature_dimension = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("output_spatial_dimensions");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v1' to have attribute 'output_spatial_dimensions' of type '::mlir::Attribute'";
        });
      }
      output_spatial_dimensions = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("feature_group_count");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v1' to have attribute 'feature_group_count' of type '::mlir::Attribute'";
        });
      }
      feature_group_count = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("batch_group_count");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v1' to have attribute 'batch_group_count' of type '::mlir::Attribute'";
        });
      }
      batch_group_count = tblgen_attr;
    }
    {
      auto tblgen_attr = op0->getAttrOfType<::mlir::Attribute>("precision_config");(void)tblgen_attr;
      if (!(tblgen_attr)){
        return rewriter.notifyMatchFailure(op0, [&](::mlir::Diagnostic &diag) {
          diag << "expected op 'vhlo.dynamic_conv_v1' to have attribute 'precision_config' of type '::mlir::Attribute'";
        });
      }
      precision_config = tblgen_attr;
    }

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::vhlo::DynamicConvOpV2 tblgen_DynamicConvOpV2_0;
    {
      ::llvm::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::llvm::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*lhs.begin()));
      tblgen_values.push_back((*rhs.begin()));
      tblgen_values.push_back((*d_padding.begin()));
      if (auto tmpAttr = window_strides) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("window_strides"), tmpAttr);
      }
      if (auto tmpAttr = lhs_dilation) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("lhs_dilation"), tmpAttr);
      }
      if (auto tmpAttr = rhs_dilation) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("rhs_dilation"), tmpAttr);
      }
      if (auto tmpAttr = window_reversal) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("window_reversal"), tmpAttr);
      }
      if (auto tmpAttr = input_batch_dimension) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("input_batch_dimension"), tmpAttr);
      }
      if (auto tmpAttr = input_feature_dimension) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("input_feature_dimension"), tmpAttr);
      }
      if (auto tmpAttr = input_spatial_dimensions) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("input_spatial_dimensions"), tmpAttr);
      }
      if (auto tmpAttr = kernel_input_feature_dimension) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("kernel_input_feature_dimension"), tmpAttr);
      }
      if (auto tmpAttr = kernel_output_feature_dimension) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("kernel_output_feature_dimension"), tmpAttr);
      }
      if (auto tmpAttr = kernel_spatial_dimensions) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("kernel_spatial_dimensions"), tmpAttr);
      }
      if (auto tmpAttr = output_batch_dimension) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("output_batch_dimension"), tmpAttr);
      }
      if (auto tmpAttr = output_feature_dimension) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("output_feature_dimension"), tmpAttr);
      }
      if (auto tmpAttr = output_spatial_dimensions) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("output_spatial_dimensions"), tmpAttr);
      }
      if (auto tmpAttr = feature_group_count) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("feature_group_count"), tmpAttr);
      }
      if (auto tmpAttr = batch_group_count) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("batch_group_count"), tmpAttr);
      }
      if (auto tmpAttr = precision_config) {
        tblgen_attrs.emplace_back(rewriter.getStringAttr("precision_config"), tmpAttr);
      }
      ::llvm::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_DynamicConvOpV2_0 = rewriter.create<::mlir::vhlo::DynamicConvOpV2>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_DynamicConvOpV2_0.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  };
};

void LLVM_ATTRIBUTE_UNUSED populateWithGenerated(::mlir::RewritePatternSet &patterns) {
  patterns.add<DynamicConvDowngradeV2ToV1>(patterns.getContext());
  patterns.add<DynamicConvUpgradeV1ToV2>(patterns.getContext());
}
